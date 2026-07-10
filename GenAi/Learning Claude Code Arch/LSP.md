### Enhancing Claude Code with LSP
_Tags: #claude-code #lsp #dev-tools #productivity #setup_

> [!summary] TL;DR
> 
> By default, Claude Code uses text-based search (`grep`), which is slow (30-60s) and inaccurate. Enabling the **Language Server Protocol (LSP)** gives Claude true code intelligence, dropping query times to **~50ms** with 100% accuracy.

---

## 🧠 Core Concept: What is LSP?

Before LSP, every editor needed a custom plugin for every language (M × N problem). Microsoft created LSP to separate the editor from the language intelligence (M + N problem).

- **Editor:** Asks questions via JSON-RPC ("Where is this defined?").
    
- **Language Server:** A dedicated process that understands the language perfectly and provides the answers.
    

### The Performance Gap

|**Feature**|**Default (Grep/Glob/Read)**|**With LSP**|
|---|---|---|
|**Method**|Text Pattern Matching|Semantic JSON-RPC|
|**Accuracy**|Fuzzy (catches comments, variables)|**100% Exact**|
|**Speed**|30-60 seconds (reads every file)|**~50 milliseconds**|
|**Understanding**|Treats code as pure text|Understands structure, types, relationships|

---

## ⚡ LSP Superpowers for Claude Code

### 1. Passive: Self-Correcting Edits

The language server pushes diagnostics (type errors, missing imports) to Claude **in real-time**.

- **Workflow:** You ask for a change -> Claude edits -> LSP flags 3 errors -> Claude sees and fixes them -> You get 0 errors on the first try.
    

### 2. Active: On-Demand Code Intelligence

Claude can automatically trigger these exact operations:

- `goToDefinition`: "Where is `processOrder` defined?"
    
- `findReferences`: "Find all places that call `validateUser`."
    
- `hover`: "What type is the `config` variable?"
    
- `documentSymbol`: "List all functions in this file."
    
- `workspaceSymbol`: "Find the `PaymentService` class."
    
- `goToImplementation`: "What classes implement `AuthProvider`?"
    
- `incomingCalls` / `outgoingCalls`: Call hierarchy tracing.
---
