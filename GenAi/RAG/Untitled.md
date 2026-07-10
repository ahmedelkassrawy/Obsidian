Tip froms RAG_POC
```python
def hash_content(content:str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
```

Use 
```python
global _lc_models = {
    "llm": None,
    "embeddings": None,
    "splitter": None
}
```

Processing document
```python
async def process_documents_langchain(db: Session, file_bytes: bytes, file_name: str, file_type: str):
    text = extract_text(file_bytes, file_type)
    content_hash = hash_content(text)

    # 2. Duplicate Check
    existing = db.query(Document).filter(Document.content_hash == content_hash).first()
    if existing:
        return existing.id

    _init_langchain_models()

    # 3. Create Record
    new_doc = Document(id=uuid.uuid4(), filename=file_name, filetype=file_type, content_hash=content_hash)
    db.add(new_doc)
    db.flush()

    chunks = _lc_models["splitter"].split_text(text)
    
    logger.info(f"Embedding {len(chunks)} chunks...")
    embeddings = _lc_models["embeddings"].embed_documents(chunks)

    # 6. Bulk Save
    chunks_to_add = [
        DocumentChunk(
            id=uuid.uuid4(),
            document_id=new_doc.id,
            content=chunk_text,
            embedding=vector
        )
        for chunk_text, vector in zip(chunks, embeddings)
    ]
    
    db.bulk_save_objects(chunks_to_add)
    db.commit()
    
    return new_doc.id
```

Stream
```python
@router.post("/chat/stream")
async def chat_stream_endpoint(request: AskRequest, db: Session = Depends(get_db)):
    """Streaming version of the chat endpoint"""
    try:
        # Chat handle
        if request.chat_id is None or str(request.chat_id).strip() == "":
            new_chat = Chat(
                id=uuid.uuid4(),
                title=request.question[:30]
            )
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            chat_id = new_chat.id
            chat_history = []
        else:
            chat_id = uuid.UUID(str(request.chat_id))
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if chat is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat not found"
                )
            chat_history = get_chat_history(db, chat_id)

        # Rewrite query
        rewritten_query = await rewrite_query_with_history(chat_history, request.question)
        logger.info(f"Rewritten query: {rewritten_query}")

        # Get chunks
        relevant_chunks = await retrieve_relevant_chunks(db, rewritten_query)
        context_snippets = [chunk.content for chunk in relevant_chunks]
        sources = list(set([chunk.document.filename for chunk in relevant_chunks]))

        # Save user message
        user_msg = ChatMessage(
            chat_id=chat_id,
            role="user",
            content=request.question
        )
        db.add(user_msg)
        db.commit()

        # Stream generator
        async def generate_stream():
            full_response = ""
            
            # Send initial metadata
            yield f"data: {json.dumps({'type': 'metadata', 'chat_id': str(chat_id), 'sources': sources})}\n\n"
            
            # Stream the response
            async for chunk in rag_async_stream(
                question=rewritten_query,
                context_snippets=context_snippets,
                sources=sources,
                chat_history=chat_history
            ):
                full_response += chunk
                yield f"data: {json.dumps({'type': 'content', 'chunk': chunk})}\n\n"
            
            # Save assistant message to DB
            assistant_msg = ChatMessage(
                chat_id=chat_id,
                role="assistant",
                content=full_response,
                citations={"sources": sources}
            )
            db.add(assistant_msg)
            db.commit()
            
            # Send completion signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        return StreamingResponse(generate_stream(), media_type="text/event-stream")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Chat stream error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```