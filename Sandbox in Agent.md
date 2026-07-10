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