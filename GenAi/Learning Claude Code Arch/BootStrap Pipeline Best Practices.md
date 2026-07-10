## What Startup Teaches About System Design

The bootstrap pipeline is a study in narrowing scopes. Each phase reduces the space of possibilities:

- Phase 0 narrows from “any CLI invocation” to “needs full bootstrap”
- Phase 1 narrows from “everything must load” to “load in parallel with I/O”
- Phase 2 narrows from “unknown environment” to “trusted, configured environment”
- Phase 3 narrows from “no capabilities” to “fully registered”
- Phase 4 narrows from “seven possible modes” to “one concrete launch path”

By the time the REPL renders, every decision has been made. The query loop receives a fully configured environment with no ambiguity about what mode it is in, which tools are available, or what permissions apply. The 300ms budget is not just a performance target — it is a forcing function that prevents bootstrap from becoming a lazy initialization system where decisions are deferred and scattered throughout the codebase.

---

## Apply This

**Overlap I/O with initialization.** Fire slow operations (subprocess spawns, credential reads, network checks) at module evaluation time, before they are needed. The JavaScript engine is doing synchronous work anyway — use that time for parallel I/O. The pattern: `const promise = startSlowThing()` at the top of the file, `await promise` at the point of use.

**Narrow scope as early as possible.** The bootstrap pipeline’s five files form a funnel: each phase eliminates work that subsequent phases do not need to do. Fast-path dispatch is the most dramatic example, but the principle applies everywhere. If you can determine at parse time that a code path is unnecessary, skip it.

**Establish trust boundaries explicitly.** If your application reads from an environment it does not control (environment variables, configuration files, shell settings), draw a clear line between “safe to read before the user consents” and “only read after consent.” The trust boundary prevents a class of attacks where a malicious environment poisons the application before the user has a chance to evaluate it.

**Memoize your init function.** Make initialization idempotent — calling it twice produces the same result. This eliminates ordering bugs when multiple entry points may each trigger initialization. The memoization pattern is trivial but eliminates an entire class of double-initialization bugs.

**Capture early input before yielding.** In an event-driven system, user input that arrives during initialization can be lost. Claude Code captures the initial prompt from argv before any async work begins, ensuring that `claude "fix the bug"` does not drop the prompt if initialization takes longer than expected.