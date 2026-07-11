# Context Compression - Claude Code

## Summary

Four main context compaction strategies work together in a query loop to manage conversation history and prevent exceeding token limits:

| Strategy | Trigger | Purpose |
|----------|---------|---------|
| **Snip Compact** | Feature flag (HISTORY_SNIP) | Removes messages from history early |
| **Microcompact** | Time-based or cache-based | Removes redundant tool outputs |
| **Context Collapse** | Feature flag (CONTEXT_COLLAPSE) | Granular summaries instead of full compaction |
| **Auto-compact** | Token threshold | Summarizes conversation when token count exceeds limit |

**Execution Order in Query Loop:**
1. Snip compact → 2. Microcompact → 3. Context Collapse → 4. Auto-compact

---

## Python Implementation

```python
# Python Implementation of Context Compression Concepts

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class QuerySource(Enum):
    SESSION_MEMORY = "session_memory"
    COMPACT = "compact"
    MARBLE_ORIGAMI = "marble_origami"
    REPL_MAIN_THREAD = "repl_main_thread"


@dataclass
class TokenWarningState:
    percent_left: int
    is_above_warning_threshold: bool
    is_above_error_threshold: bool
    is_above_auto_compact_threshold: bool
    is_at_blocking_limit: bool


WARNING_THRESHOLD_BUFFER_TOKENS = 10000
ERROR_THRESHOLD_BUFFER_TOKENS = 2000
MANUAL_COMPACT_BUFFER_TOKENS = 5000
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3


class ContextCompression:
    def __init__(self, auto_compact_enabled: bool = True, context_collapse_enabled: bool = False):
        self.auto_compact_enabled = auto_compact_enabled
        self.context_collapse_enabled = context_collapse_enabled
        self.consecutive_failures = 0
    
    def calculate_token_warning_state(
        self,
        token_usage: int,
        model: str,
    ) -> TokenWarningState:
        """Calculate token warning thresholds."""
        auto_compact_threshold = self._get_auto_compact_threshold(model)
        threshold = auto_compact_threshold if self.auto_compact_enabled else self._get_effective_context_window_size(model)
        
        percent_left = max(0, round(((threshold - token_usage) / threshold) * 100))
        
        warning_threshold = threshold - WARNING_THRESHOLD_BUFFER_TOKENS
        error_threshold = threshold - ERROR_THRESHOLD_BUFFER_TOKENS
        
        is_above_warning = token_usage >= warning_threshold
        is_above_error = token_usage >= error_threshold
        is_above_auto_compact = self.auto_compact_enabled and token_usage >= auto_compact_threshold
        
        actual_context_window = self._get_effective_context_window_size(model)
        blocking_limit = actual_context_window - MANUAL_COMPACT_BUFFER_TOKENS
        is_at_blocking = token_usage >= blocking_limit
        
        return TokenWarningState(
            percent_left=percent_left,
            is_above_warning_threshold=is_above_warning,
            is_above_error_threshold=is_above_error,
            is_above_auto_compact_threshold=is_above_auto_compact,
            is_at_blocking_limit=is_at_blocking,
        )
    
    def should_auto_compact(
        self,
        messages: list,
        model: str,
        query_source: Optional[QuerySource] = None,
        snip_tokens_freed: int = 0,
    ) -> bool:
        """Determine if auto-compaction should trigger."""
        # Recursion guards
        if query_source in [QuerySource.SESSION_MEMORY, QuerySource.COMPACT]:
            return False
        
        # Context collapse mode check
        if self.context_collapse_enabled:
            if query_source == QuerySource.MARBLE_ORIGAMI:
                return False
        
        if not self.auto_compact_enabled:
            return False
        
        # Context collapse owns the headroom problem
        if self.context_collapse_enabled:
            if self._is_context_collapse_enabled():
                return False
        
        token_count = self._token_count_with_estimation(messages) - snip_tokens_freed
        threshold = self._get_auto_compact_threshold(model)
        
        warning_state = self.calculate_token_warning_state(token_count, model)
        return warning_state.is_above_auto_compact_threshold
    
    def auto_compact_if_needed(
        self,
        messages: list,
        tool_use_context: dict,
        query_source: Optional[QuerySource] = None,
    ) -> dict:
        """Execute compaction if needed."""
        if self.consecutive_failures >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES:
            return {"was_compacted": False}
        
        model = tool_use_context.get("main_loop_model", "claude-3-5-sonnet-20241022")
        should_compact = self.should_auto_compact(messages, model, query_source)
        
        if not should_compact:
            return {"was_compacted": False}
        
        try:
            compaction_result = self._compact_conversation(messages, tool_use_context)
            self.consecutive_failures = 0
            return {
                "was_compacted": True,
                "compaction_result": compaction_result,
            }
        except Exception as e:
            self.consecutive_failures += 1
            return {"was_compacted": False, "consecutive_failures": self.consecutive_failures}
    
    # Helper methods (placeholders)
    def _get_auto_compact_threshold(self, model: str) -> int:
        thresholds = {
            "claude-3-5-sonnet-20241022": 150000,
            "claude-3-opus-20240229": 200000,
        }
        return thresholds.get(model, 100000)
    
    def _get_effective_context_window_size(self, model: str) -> int:
        windows = {
            "claude-3-5-sonnet-20241022": 200000,
            "claude-3-opus-20240229": 200000,
        }
        return windows.get(model, 100000)
    
    def _token_count_with_estimation(self, messages: list) -> int:
        total = 0
        for msg in messages:
            if isinstance(msg, dict):
                content = str(msg.get("content", ""))
            else:
                content = str(msg)
            total += len(content) // 4
        return total
    
    def _is_context_collapse_enabled(self) -> bool:
        return self.context_collapse_enabled
    
    def _compact_conversation(self, messages: list, context: dict) -> dict:
        return {" compacted": True, "message_count": len(messages)}


class Microcompact:
    def __init__(self):
        self.cached_mc_state = {}
    
    def microcompact_messages(
        self,
        messages: list,
        tool_use_context: Optional[dict] = None,
        query_source: Optional[QuerySource] = None,
    ) -> dict:
        """Main entry point for microcompaction."""
        time_result = self._maybe_time_based_microcompact(messages, query_source)
        if time_result:
            return time_result
        
        return {"messages": messages}
    
    def _maybe_time_based_microcompact(
        self,
        messages: list,
        query_source: Optional[QuerySource] = None,
    ) -> Optional[dict]:
        """Time-based trigger for clearing old tool results."""
        gap_threshold_minutes = 30
        keep_recent = 2
        
        gap_minutes = self._calculate_time_gap(messages)
        
        if gap_minutes is None or gap_minutes < gap_threshold_minutes:
            return None
        
        compactable_ids = self._collect_compactable_tool_ids(messages)
        
        if len(compactable_ids) <= keep_recent:
            return None
        
        keep_set = set(compactable_ids[-keep_recent:])
        clear_set = set(id for id in compactable_ids if id not in keep_set)
        
        if not clear_set:
            return None
        
        result_messages = []
        for message in messages:
            if isinstance(message, dict) and message.get("type") == "user":
                new_content = []
                for block in message.get("content", []):
                    if (
                        block.get("type") == "tool_result"
                        and block.get("tool_use_id") in clear_set
                    ):
                        new_content.append({**block, "content": "[tool result cleared]"})
                    else:
                        new_content.append(block)
                result_messages.append({**message, "content": new_content})
            else:
                result_messages.append(message)
        
        return {"messages": result_messages}
    
    def _calculate_time_gap(self, messages: list) -> Optional[float]:
        return None
    
    def _collect_compactable_tool_ids(self, messages: list) -> list:
        tool_ids = []
        for msg in messages:
            if isinstance(msg, dict) and msg.get("type") == "user":
                for block in msg.get("content", []):
                    if block.get("type") == "tool_result":
                        tool_id = block.get("tool_use_id")
                        if tool_id:
                            tool_ids.append(tool_id)
        return tool_ids


def query_loop(
    messages: list,
    tool_use_context: dict,
    features: dict,
) -> list:
    """Main query loop with context compression pipeline."""
    compression = ContextCompression(
        auto_compact_enabled=features.get("auto_compact", True),
        context_collapse_enabled=features.get("context_collapse", False),
    )
    microcompact = Microcompact()
    
    messages_for_query = messages.copy()
    
    # 1. Snip compact (if enabled)
    if features.get("history_snip"):
        messages_for_query = _apply_snip_compact(messages_for_query)
    
    # 2. Microcompact
    microcompact_result = microcompact.microcompact_messages(
        messages_for_query,
        tool_use_context,
    )
    messages_for_query = microcompact_result["messages"]
    
    # 3. Context collapse (if enabled)
    if features.get("context_collapse"):
        messages_for_query = _apply_context_collapse(messages_for_query, tool_use_context)
    
    # 4. Auto-compact
    compact_result = compression.auto_compact_if_needed(
        messages_for_query,
        tool_use_context,
    )
    if compact_result["was_compacted"]:
        messages_for_query = compact_result["compaction_result"].get("messages", messages_for_query)
    
    return messages_for_query


def _apply_snip_compact(messages: list) -> list:
    return messages


def _apply_context_collapse(messages: list, context: dict) -> list:
    return messages


if __name__ == "__main__":
    sample_messages = [
        {"type": "user", "content": "Hello"},
        {"type": "assistant", "content": "Hi there!"},
        {"type": "user", "content": [{"type": "tool_result", "tool_use_id": "tool_1", "content": "result"}]},
    ]
    
    features = {"auto_compact": True, "context_collapse": False, "history_snip": False}
    context = {"main_loop_model": "claude-3-5-sonnet-20241022"}
    
    result = query_loop(sample_messages, context, features)
    print(f"Processed {len(result)} messages")
```

---

## Key Concepts

- **Circuit Breaker**: `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` prevents infinite retry loops
- **Token Warning States**: percentLeft, warningThreshold, errorThreshold, autoCompactThreshold, blockingLimit
- **Feature Flags**: HISTORY_SNIP, CACHED_MICROCOMPACT, CONTEXT_COLLAPSE, REACTIVE_COMPACT
- **Post-Compact Cleanup**: Resets caches, clears states, handles memory files


## Apply This: Building Your Own Agent Loop

**Use a generator, not callbacks.** The backpressure is free. The return value semantics are free. The composability via `yield*` is free. Agent loops are strictly forward-moving — you never need to rewind or fork.

**Make state transitions explicit.** Reconstruct the full state object at every `continue` site. The verbosity is the feature — it prevents partial-update bugs and makes each transition self-documenting.

**Withhold recoverable errors.** If your consumers disconnect on errors, do not yield errors until you know recovery has failed. Push them to an internal buffer, attempt recovery, and surface only on exhaustion.

**Layer your context management.** Light operations first (removal), heavy operations last (summarization). This preserves granular context when possible and falls back to monolithic summaries only when necessary.

**Add circuit breakers for every retry.** Every recovery mechanism in `query.ts` has an explicit limit: 3 auto-compact failures, 3 max-output recovery attempts, 1 reactive compact attempt. Without these limits, the first production session that triggers a retry-on-failure loop will burn your API budget overnight.