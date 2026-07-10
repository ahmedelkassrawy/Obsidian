Tools Schema Best Practices
Do ✅	Don't ❌
Use .describe() on every field	Leave fields undescribed
Provide examples in descriptions	Use vague descriptions
Use .optional() for optional fields	Make everything required
Use semantic wrappers for flexibility	Be overly strict
Add constraints (min, max)	Allow any value
Use .refine() for complex validation	Try to validate in execute()

Advanced Tool Patterns
1. Streaming Results
2. Background Execution
BashTool can run commands in background
3. File State Caching
Tools can cache file reads for efficiency:

async execute(input, context) {
  // Check cache first
  const cached = context.readFileCache.get(input.file_path)
  if (cached && !cached.isStale()) {
    return cached.content
  }

  // Read and cache
  const content = await fs.readFile(input.file_path, 'utf-8')
  context.readFileCache.set(input.file_path, content)

  return content
}

4. Sub-Agent Spawning
AgentTool spawns sub-agents for complex tasks:

async execute(input, context) {
  const agent = await spawnAgent({
    type: input.subagent_type,
    prompt: input.prompt,
    tools: selectToolsForAgent(input.subagent_type)
  })

  // Wait for agent to complete
  const result = await agent.run()

  return result
}

Returning Errors vs Throwing
Return Error Object	Throw Exception
Claude can see error details	Tool execution stops
Claude can retry with changes	User sees error message
Graceful degradation	Hard failure
Preferred for recoverable errors	For unrecoverable errors
Example - Returning error:

// GOOD: Claude can see this and adjust
return {
  success: false,
  error: "File not found: app.ts",
  suggestion: "Did you mean app.tsx?"
}
Example - Throwing error:

// ONLY for unrecoverable errors
throw new Error("Out of memory")

5. Concurrency & Parallel Execution
Tools can declare themselves safe for parallel execution by implementing concurrency checks:

// In tool definition
isConcurrencySafe(input) {
  return this.isReadOnly?.(input) ?? false;
}

6. Semantic Zod Types for LLM Robustness
Use internal helpers like `semanticBoolean` and `semanticNumber` over primitive Zod types. This handles edge cases where the LLM might pass a string "true" instead of a boolean `true`, ensuring the tool doesn't fail on parsing.

run_in_background: semanticBoolean(z.boolean().optional())
timeout: semanticNumber(z.number().optional())

7. Fine-Grained Permissions and Validation
Tools should implement custom validation and permission matchers before execution to fail fast and prevent unsafe operations.

async validateInput(input, context) {
  if (isUnsafe(input)) {
    return { result: false, message: "Blocked: Unsafe operation", errorCode: 10 }
  }
  return { result: true }
}

### 

Best practices for custom tool definitions

- **Provide extremely detailed descriptions.** This is by far the most important factor in tool performance. Your descriptions should explain what the tool does, when it should be used (and when it shouldn't), what each parameter means and how it affects the tool's behavior, and any important caveats or limitations. The more context you can give Claude about your tools, the better it will be at deciding when and how to use them. Aim for at least 3-4 sentences per tool description, more if the tool is complex.
- **Consolidate related operations into fewer tools.** Rather than creating a separate tool for every action (`create_pr`, `review_pr`, `merge_pr`), group them into a single tool with an `action` parameter. Fewer, more capable tools reduce selection ambiguity and make your tool surface easier for Claude to navigate.
- **Use meaningful namespacing in tool names.** When your tools span multiple services or resources, prefix names with the resource (e.g., `db_query`, `storage_read`). This makes tool selection unambiguous as your library grows.
- **Design tool responses to return only high-signal information.** Return semantic, stable identifiers (e.g., slugs or UUIDs) rather than opaque internal references, and include only the fields Claude needs to reason about its next step. Bloated responses waste context and make it harder for Claude to extract what matters.