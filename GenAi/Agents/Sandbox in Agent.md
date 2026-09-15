---
description: "Sketch of a two-layer agent sandbox: a Docker container per deployed agent, and a bubblewrap sandbox per bash tool call."
domain: ai-eng
type: concept
status: stub
tags:
  - domain/ai-eng
  - type/concept
  - status/stub
  - topic/agents
  - topic/ai-security
aliases:
  - "sandbox"
  - "bubblewrap"
  - "agent isolation"
hubs:
  - "[[Agents]]"
  - "[[AI Security]]"
---
Two Layer Arch
GCP as the outer layer covering
	Layer 1 -> Docker Container (one per deployed agent)
		Docker isolates agents from each other + host
	 Layer 2 ->  Bubble Wrap Sandbox (BWRAP) one per bash tool call
		 Isolates bash from the agents own secrets

![[Pasted image 20260503024359.png]]
![[Pasted image 20260503024511.png]]

![[Pasted image 20260503024516.png]]
![[Pasted image 20260503024745.png]]

![[Pasted image 20260503024749.png]]
![[Pasted image 20260503024834.png]]