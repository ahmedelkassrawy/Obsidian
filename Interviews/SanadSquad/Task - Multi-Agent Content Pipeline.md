Build a small AI sys that creates one week of X posts for a smart contract security company 

Business Logic
- Smart Contract -> a program that runs on a blockchain. Bugs in that program can let someone steal funds , lock funds or manipulate behaviour

An audit firm on them examines these programs to find secuirty problems

Our sys will create content for that kind of firm
- Educational -> explain vulnerabilites and how they happen.
- Marketing Content -> explain the firms value and encourage potential customers to use it as a services

So its an Automated Content Workflow

Is it an agent or a workflow?
-> Its a workflow , its just some steps one after another so we dont need the LLM to decide where we should go , even the retry and fails are not left foor our decision

Orchestrator -> 

Whats the workflow?
-> Plan -> Research -> Write -> Validator -> Review -> Visual -> Report

-> Plan comes from the user as slots
-> if the slot is empty -> the llm should recommend a new topic and research about it
-> if the slot is unempty we go also to the research node

-> the researcher node goes to the knowledge bank as the no 1 priorty and then the web search and ranking them with the metadata having the source link which will be used in the tweets or in the review phase 
-> writer -> technical thread writer ( 5 to 10 tweets ) 
			- > marketing post writer
-> validator is the all python mighty where it validates the em dashes and all the things we want to remove 
-> Reviewwer -> scores every piece against a rubic list of things we are looking for anf should provide a reason to reject
->Vislaizer -> makes an image for each piece, or a written image spec if you have no image API.

