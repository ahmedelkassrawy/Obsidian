Where a tool's response when a bad or imperfect input -> **gives the LLM everything it needs to recover on its very next step — automatically, silently, and without bothering the user.**

LLM calling a tool  problems:
- Every extra round trip is expesive and slow 
- Dead-end errors make the models panic or leak plumbing 

So a tool error is not a crash report — it is a steering prompt for the model's next turn.

---
