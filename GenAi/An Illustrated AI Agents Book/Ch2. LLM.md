LLM power agents to go from observations to actions

Autoregressive models -> the ones that output text is actually a loop where the text is predicted one after another , and then added as input and then we process the new input again to generate next token.

For an LLM to be able to power an agent, it needs an additional set of capabilities to fit the expected role. LLM creators train LLMs in the subsequent phase of training, called posttraining, to be able to parse inputs and generate outputs in a format that supports these expected capabilities