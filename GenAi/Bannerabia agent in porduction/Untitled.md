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