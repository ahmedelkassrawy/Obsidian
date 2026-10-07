Each tenant has an id, each tenant has the document and chunked
So we have to ingest first the pdf or the file into the correct tenant and then chunk them using the Recusrive char splitter and then these chunks everyone takes an id and has the metadata of the source which is the document id and then embed them using the embedder 
SO after that we can do the indexing based on the chunks id 
and the hybrid bm25+cosine simliarity and then reranking them and using the redis semantic caching -> for the agent and the rag 