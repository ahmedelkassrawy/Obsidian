AI Engineering is actually just regular software engineering wrapped around an LLM 

1. User Input (messgae + optional PDF/Photo + wchi app page they are on)
2. Server guardrails (Determinstic Code )
	- Auth and Brand isolation (which brands/workspace can this user touch)
		- Approval check (did the user say "approve" to pending preview?)
3. Context Assembly (Building API Request)
[ Tool Schemas ] + [ System Prompt ] + [ Dynamic Tail ] + [ Chat History ] + [ New Message ]
4. Agent Loop (LLM <-> Tools)
	LLM reads the full request ──► decides to call a tool (e.g. stage_draft)
	 Server runs tool safely ──► returns tool result text back into context 
	 LLM reads result ──► writes reply (or calls another tool)
5. Post-Processing and UI  (Determinstic)
	- Render interactive Cards and safe suggestion chips
	- Persist history & usage metrics
	- Wait for human approval before anything publishes

What was wrong 
- Wasted money 
- Unnecessary back-to-forth turns 
- conflicting instrcuctions
- missing memory

1. Prompt Caching and Prefix Layout
Money and cost leak , since the providers offer prompt caching where if the beginning (prefix) of your request is **byte for byte** identical for a recent request up to a cache breakpoint we pay 0.1% to read instead of 1.25x to write it fresh 

The golden rule of prompt caching is: 
**static content first, dynamic content last.** If _even one character_ changes early in the prompt, everything after it misses the cach