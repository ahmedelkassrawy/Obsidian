AI agents are capable of autonomosuly deciding which actions to take, when to take and even how

What is an AI Agent
An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators.

Enviroment -> World the agent interacts with
Sesnors -> to observe the enviroment
Actuators -> tools the agents use to interact the enviroment 
Agent Program -> brain or rules the agent uses to decide how to for from observations to actions

![[Pasted image 20261024165042.png]]

What are LLMs?
The LLM processes these tokens, and a prediction is made on what the next token could be

Query -> Tokens -> Token Probability -> Output

Autoregression -> iteratively LLM predicting the next token and uses the predicted token to update its input , then continues the predictions

![[Pasted image 20261024165432.png]]

Train-Time scaling -> where training on more data and making models larger led to reliable , predictable improvements in performance

- The idea was that pre-training, the first and most expensive stage of training an LLM, was where the gains came from: 
- the larger your pre-training budget, the better the resulting model

Input -> More data , Pre-Training -> More compute , Base Model -> more params

Training simply became too expensive for the small increase in performance

Thinking and Reasoning was introduced after it was thinking implcitly and just showing the answer , the main idea was to allow LLMS to write down their thoughts first through their autoregressive behaviour before coming to an answer

Memory 
Multiturn conversations expose a vital flow of LLMs that they forget entities and dont remember
"Stateless" -> inforamtion is not presisted across calls

Information Overload -> if LLM receieve a lot of info , it becomes difficult to process and poor decision making 

Tools 
LLMs are not capable of using the tools by themselves
But LLMs can be dealt with as functions that take input and give output
LLM can only describe the intent of taking the action when outputting text,

So by recieving the text "What is 5.1 times 7.3" it generates "multiply(5.1,7.3)"

This string merely represents the LLM’s intention to take an action, but the action itself is not taken without outside intervention

will need to write software to convert that text into an action
If the LLMs ouput were JSOn we woulkd use that to choose the correct tool and fill in parameters

Input -> LLM -> JSON Ouput -> Tool filled params after reading the JSON -> Tool Output -> LLM -> Output

Planning and reflections
from regular LLM to an AI agent is the ability of plan and reflect,
the agent will need to decide which steps to take and how to take them and when

Involves breaking down a larger task into smaller ones

But creating a plan is not sufficient. The LLM might discover halfway through its plan that some of its steps might not be appropriate.

By reflecting on past behavior, agents can attempt to uncover their faults and make attempts to fix them. Therefore, the initial plan can be continuously improved.

n create an iterative loop of planning out tasks, taking actions, and reflecting on the output

![[Pasted image 20261024173341.png]]

An Agentic System With all these components, a reasoning LLM augmented with memory, tools, and planning, we arrive at the next stage of the agent: 
	the way it behaves inside a system. 
	
This covers common use cases, degree of autonomy, ethical considerations, and how these agents and systems can be evaluated

Autonomy
The freedom where LLM can choose betwen the tools,decide to update the intial plan or add aditional steps or stop 

a system is more “agentic” the more the LLM has full control over its actions.

However, we believe that as long as the agent exhibits goal-directed behavior and makes decisions, we can call it an agent.