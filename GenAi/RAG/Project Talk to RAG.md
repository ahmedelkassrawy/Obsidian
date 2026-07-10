The pipeline for RAG consists of the following stages:
1. Extraction of documents from a filesystem to load the textual content in chunks onto memory.
2. Transformation of the textual content by cleaning, splitting, and preparing them to be passed into an embedding model to produce embedding vectors that represent a chunk’s semantic meaning
3. Storage of embedding vectors alongside metadata, such as the source and text chunk, in a vector store such as Qdrant
4. Retrieval of semantically relevant embedding vectors by performing a semantic search on the user’s query to the LLM. The original text chunks— stored as metadata of the retrieved vectors— are then used to augment (i.e., enhance the context within) the initial prompt provided to the LLM.
5. Generation of LLM response bypassing both the query and retrieved chunks (i.e., context) to the LLM for getting a response

 ![[Pasted image 20260122223614.png]]

![[Pasted image 20260122223634.png]]

---
### 1st Step: Implement File Uploading
Using FastAPI’s UploadFile class, you can accept documents from users in chunks and save them into the filesystem or any other file storage solution such as a blob storage. The important item to note here is that this I/O operation is nonblocking through asynchronous programming, which FastAPI’s UploadFile class supports.
```python
$ pip install aiofiles python-multipart
```

upload.py
```python
import os
import aiofiles 
from aiofiles.os import makedirs
from fastapi import UploadFile

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50 #50 MB

async def save_file(file: UploadFile) -> str:
    await makedirs("uploads", exist_ok = True)
    
    file_path = os.path.join("uploads",file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(DEFAULT_CHUNK_SIZE):
            await f.write(chunk)

    return file_path
```

main.py
```python
from fastapi import FastAPI,HTTPException,status,UploadFile,File
from typing import Annotated
from upload import save_file

app = FastAPI()

@app.post("/upload")
async def file_upload_controller(file: Annotated[UploadFile, File(description = "Uploaded PDF document")]):
    if file.content_type != "application/pdf":
        raise HTTPException(
            detail = "Invalid file type. Only PDF Files are allowed.",
            status_code = status.HTTP_400_BAD_REQUEST,
        )
    
    try:
        await save_file(file)
    except Exception as e:
        raise HTTPException(
            detail = f"An error occurred while saving the file: {str(e)}",
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    return {
        "filename":file.filename,
        "message": "File uploaded successfully."
    }
```

---
#### Step 2: Data Transformation
![[Pasted image 20260122232512.png]]

Extractor , Loader, TextSplitter, Embedder

extractor.py
```python
from pypdf import PdfReader

def pdf_text_extractor(filepath:str) -> None:
    content = ""

    pdf_reader = PdfReader(filepath,strict = True)

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            content += f"{page_text}\n\n"

    with open(filepath.replace("pdf","txt"), "w",encoding = "utf-8") as file:
        file.write(content)
```

- Loop over every page in the PDF document, and extract and append all text content into a long string. 

- Write the content of the PDF document into a text file for downstream processing. Specify encoding="utf-8" to avoid problems on platforms like Windows.

transform.py
```python
import re
from typing import Ant,AsyncGenerator
import aiofiles
from transformers import AutoModel

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50

embedder = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-base-en",trust_remote_code=True)

async def load(filepath:str) -> AsyncGenerator[str,Any]:
    async with aiofiles.open(filepath,"r",encoding = "utf-8") as f:
        while chunk := await f.read(DEFAULT_CHUNK_SIZE): #3
            yield chunk #4

def clean_text(text:str) -> str:
    t = text.replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\. ,", "", t)
    t = t.replace("..", ".")
    t = t.replace(". .", ".")
    cleaned_text = t.replace("\n", " ").strip()
    return cleaned_text 

def embed(text:str) -> list[float]:
    return embedder.encode(text).tolist() #5
```

- Use the aiofiles library to open an asynchronous connections to a file on the filesystem
- 3 -> Load the content of text documents in chunks for memory-efficient I/O operation.
- 4 -> Instead of returning a chunk , yield it so that the load() function becomes an asynchronous generator. Asynchronous generators can be iterated with async for loop s so that blocking operations within them can be await ed to let the event loop start/resume other tasks. Both async for loops and normal for loops, iterate sequentially over the iterable but async for loops allow for iteration over an async iterator.
- 5 -> Use the model to encode the text and then use the tolist( ) to an embedding vector

Once the data is processed into embedding vectors, you can store them into the vector database

repository.py
```python
from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import ScoredPoint

class VectorRepository:
    def __init__(self, host:str = "localhost",
                port:int = 6333) -> None:
        self.db_client = AsyncQdrantClient(host = host,port = port)

    async def create_collection(self,collection_name:str, size:int) -> bool:
        vector_config = models.VectorParams(
            size = size,
            distance = models.Distance.COSINE
        )
        response = await self.db_client.get_collections()

        #check if collections exist
        collection_exists = any(collection.name == collection_name 
                            for collection in response.collections)
        
        if collection_exists:
            logger.debug(f"Collection {collection_name} already exists.")
            await self.db_client.delete_collection(collection_name)
            return await self.db_client.create_collection(
                collection_name = collection_name,
                vectors_config = vector_config,
            )

        logger.debug(f"Creating collection {collection_name}.")
        return await self.db_client.create_collection(
            collection_name = collection_name,
            vectors_config = vector_config,
        )

    async def delete_collection(self,collection_name:str) -> bool:
        logger.debug(f"Deleting collection {collection_name}.")
        return await self.db_client.delete_collection(collection_name)

    async def create(self,collection_name:str,
                    embedding_vector: list[float], original_text:str,
                    source:str) -> None:
        response = await self.db_client.count(collection_name)
        logger.debug(f"Creating new vector with ID {response.count} in collection {collection_name}.")

        await self.db_client.upsert(
            collection_name = collection_name,
            points = [ 
                models.PointStruct(
                    id = response.count,
                    vector = embedding_vector,
                    payload = {
                        "source":source,
                        "original_text": original_text
                    }
                )
            ]
        )

    async def search(self,collection_name:str,query_vector: list[float],
                    retrieval_limit: int, score_threshold: float) -> list[ScoredPoint]:
        response = await self.db_client.query_points(
            collection_name = collection_name,
            query_vector = query_vector,
            limit = retrieval_limit,
            score_threshold = score_threshold
        )
        return response.points
```

>[!tip] 
Currently, converting text to embedding vectors is an irreversible process. Therefore, you will need to store the text that created the embedding with the embedding vector as metadata 

