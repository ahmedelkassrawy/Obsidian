R -> Retrieve is the step where we retrieve the information that is most relevant to the query
A -> Augmentation where we say that the retrieved info is added to the prompt and in that sense , augments the LLM internal knowledge with additional facts
G -> Generation using the prompt that include the retrieved info and the query asked

Prompt Structure for RAG
- System Instructions - How the model behaves and includes the Rules
- Developer Instructions
- Conversation History
- RAG Context
- User question

Ingestion Flow
the input data is first chunked and then embedded to be vectors and those vectors get stored at the vector db

Query Flow
the retrieval operation converts the user query to an embedding vector, and then a vector DB performs similarity search operation between the query embedding and all the possible matching vectors

once we got the retrieved facts , you instruct the LLM to produce a response that answers the query using the info in the retrieved results

>[!tip]
> Good RAG pipelines instruct the LLM to produce the references and citations so that the response includes the source of knowledge which is very good for debugging and evaluations


- How do you optimize the quality of responses by using not just vector search but also hybrid search, reranking, or other more advanced retrieval techniques? 
-  How do you incorporate information from tables, images, flowcharts, and other multimodal data into a RAG pipeline while maintaining high accuracy? 
- How do you measure the quality of your RAG pipeline—retrieval, generation, hallucination, and citations—not only on first deployment, but also continuously, as you upgrade and improve the RAG pipeline over time? 
- How can you extend your RAG to use knowledge graphs or integrate it into agentic workflows

Designing and Implementing RAG pipeline requires some DevsOps(LLMOps) best practices to ensure the low latency and strong secuirtiy
This includes the following :
- CI /CD 
	- Automated data fresh 
	- Automated Eval
	- Prompt and model controls
	- Observability
- Performance and Scalability 
	- DB Optimization
	- Optimized Inference
- Security and Governance
	- Prompt and Output Sanitization

RAG Benifits:
- Scalable and effiicient
- reduce hallucinations
- enables explainability
- Near Instant Addition and Removal of Knowledge
- Access Controls and Security