---
tags: [genai, fastapi, async, patterns, rag]
source: "Building Generative AI Services with FastAPI — Ch5 (Examples 5-4 to 5-18)"
related: "[[Ch5.Achieving Concurrency in AI Workloads]]"
---
# Ch5 — Code Patterns Worth Stealing

> [!tip] The one rule behind all of them
> `async def` is a promise to FastAPI: *"I will never block."* Break that promise and every user waits. Each pattern below is a way to keep it.

---

## 1. The `async def` trap, and the fix (Ex 5-5)

FastAPI handles the two kinds of handler differently:

- **`def` handler**: runs in a thread pool. Blocking calls are OK.
- **`async def` handler**: runs on the event loop. One blocking call freezes the **whole server**.

```python
@app.get("/block")            # ❌ async + sync client = whole server frozen
async def bad():
    return sync_client.chat.completions.create(...)

@app.get("/slow")             # ✅ OK: FastAPI sends it to the thread pool
def ok():
    return sync_client.chat.completions.create(...)

@app.get("/fast")             # ✅ best: non-blocking all the way down
async def good():
    return await async_client.chat.completions.create(...)
```

**What to steal:** when you *must* call sync code from an async handler (pypdf, a local embedding model, a sync DB driver), push it off the loop yourself:

```python
from fastapi.concurrency import run_in_threadpool   # or: asyncio.to_thread

text = await run_in_threadpool(pdf_text_extractor, filepath)
vector = await asyncio.to_thread(embed, chunk)
```

> [!warning] The book breaks its own rule later
> In Ex 5-12/5-14 it calls `embed()` (a CPU-heavy model call) directly inside `async` code. That blocks the event loop on every chunk. Wrap it as shown above.

---

## 2. Concurrent fan-out with partial-failure tolerance (Ex 5-6)

Fetch N things at once, and keep going if some of them fail:

```python
async def fetch_all(urls: list[str]) -> str:
    async with aiohttp.ClientSession() as session:          # ONE session, reused
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls],
            return_exceptions=True,                          # one failure ≠ total failure
        )
    ok = [r for r in results if isinstance(r, str)]
    if len(ok) != len(results):
        logger.warning("Some URLs could not be fetched")
    return " ".join(ok)
```

**What to steal:** `gather(..., return_exceptions=True)` + filter by type. This works for any batch: API calls, DB reads, LLM calls.

**What's missing for production:** a concurrency cap and a timeout. Without them, 500 URLs = 500 open sockets, and one slow site hangs the request forever.

```python
sem = asyncio.Semaphore(10)                                  # max 10 in flight
timeout = aiohttp.ClientTimeout(total=10)

async def fetch(session, url):
    async with sem:
        async with session.get(url, timeout=timeout) as resp:
            resp.raise_for_status()                          # 404/500 → exception, not "content"
            return parse_inner_text(await resp.text())
```

---

## 3. Dependencies as "context enrichers" that fail soft (Ex 5-7, 5-14)

The handler stays tiny. 
Each extra source of context lives in its own `Depends()` function. 
If a source breaks, it returns `""` and the main feature still works.

```python
async def get_urls_content(body: TextModelRequest = Body(...)) -> str:
    urls = extract_urls(body.prompt)
    if urls:
        try:
            return await fetch_all(urls)
        except Exception as e:
            logger.warning(f"URL fetch failed: {e}")
    return ""                                                # degrade, don't crash

@app.post("/generate/text")
async def generate(
    body: TextModelRequest,
    urls_content: str = Depends(get_urls_content),
    rag_content:  str = Depends(get_rag_content),
):
    prompt = body.prompt + " " + urls_content + rag_content
    ...
```

**What to steal:** this is a clean way to plug things into an LLM endpoint (RAG, web, user profile, memory). Adding a new context source = one new dependency + one parameter. FastAPI also runs a dependency only once per request and caches the result.

---

## 4. Streaming file upload in chunks (Ex 5-8)

```python
CHUNK = 1024 * 1024  # 1 MB

async def save_file(file: UploadFile) -> str:
    await aiofiles.os.makedirs("uploads", exist_ok=True)
    
    path = os.path.join("uploads", file.filename)
    
    async with aiofiles.open(path, "wb") as f:
        while chunk := await file.read(CHUNK):               # walrus loop = read until empty
            await f.write(chunk)
    return path
```

**What to steal:** the `while chunk := await x.read(N)` idiom. Memory stays flat no matter how big the file is.

> [!danger] Two production holes in the book's version
> 1. **Path traversal**: `file.filename` comes from the user. A filename like `../../app/main.py` writes outside `uploads/`. Use `Path(file.filename).name`, or better, a `uuid4()` name.
> 2. **No size limit**: the book's tip says to add one, but the code doesn't. Count bytes inside the loop and raise `413` past your limit.
>
> Also: `content_type` is set by the client, so anyone can fake it. Check the file's magic bytes (`%PDF`) if it matters.

---

## 5. Async generators for lazy data pipelines (Ex 5-10)

```python
async def load(filepath: str, chunk_size: int) -> AsyncGenerator[str, None]:
    async with aiofiles.open(filepath, "r", encoding="utf-8") as f:
        while chunk := await f.read(chunk_size):
            yield chunk

async for chunk in load(path, 512):          # consume with `async for`
    ...
```

**What to steal:** `yield` inside `async def` gives you a stream you can process one piece at a time, without loading everything first. The same shape works for paginated APIs, DB cursors, and LLM token streams (Ch6).

> [!note] Book inconsistency
> Ex 5-10 defines `load(filepath)` with a hard-coded 50 MB chunk, but Ex 5-12 calls `load(filepath, chunk_size)`. Add the parameter, as above.

---

## 6. ⭐ Repository + Service layering (Ex 5-11, 5-12)

This is the main design pattern of the chapter.

- **Repository** = *how* to talk to the DB (Qdrant calls, connection, collection config). It knows nothing about PDFs or RAG.
- **Service** = *what* the app does (load → clean → embed → store). It knows nothing about Qdrant's API.

That split lets you swap Qdrant for pgvector, or mock the repo in tests, without touching the business logic.

The book's code has real bugs, so here's a cleaned-up version:

```python
# rag/repository.py
import uuid
from qdrant_client import AsyncQdrantClient, models

class VectorRepository:
    def __init__(self, client: AsyncQdrantClient) -> None:
        self.client = client                                       # injected, not created here

    async def ensure_collection(self, name: str, size: int) -> None:
        if not await self.client.collection_exists(name):          # create once, never wipe
            await self.client.create_collection(
                name,
                vectors_config=models.VectorParams(size=size, distance=models.Distance.COSINE),
            )

    async def upsert_many(self, name: str, items: list[tuple[list[float], str, str]]) -> None:
        await self.client.upsert(
            collection_name=name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),                         # unique even under concurrency
                    vector=vec,
                    payload={"source": src, "original_text": text},
                )
                for vec, text, src in items
            ],
        )

    async def search(self, name: str, vector: list[float], limit: int, threshold: float):
        res = await self.client.query_points(
            collection_name=name,
            query=vector,                                          # NOT query_vector=
            limit=limit,
            score_threshold=threshold,
        )
        return res.points
```

```python
# rag/service.py
class VectorService:
    def __init__(self, repo: VectorRepository, collection: str = "knowledgebase", dim: int = 768):
        self.repo, self.collection, self.dim = repo, collection, dim  # HAS-A repo, not IS-A

    async def ingest_file(self, filepath: str, chunk_size: int = 512, batch: int = 64) -> None:
        await self.repo.ensure_collection(self.collection, self.dim)
        name, buf = os.path.basename(filepath), []
        async for chunk in load(filepath, chunk_size):
            vec = await asyncio.to_thread(embed, clean(chunk))        # keep the loop free
            buf.append((vec, chunk, name))
            if len(buf) >= batch:
                await self.repo.upsert_many(self.collection, buf); buf.clear()
        if buf:
            await self.repo.upsert_many(self.collection, buf)

    async def retrieve(self, query: str, k: int = 3, threshold: float = 0.7) -> str:
        vec = await asyncio.to_thread(embed, query)
        points = await self.repo.search(self.collection, vec, k, threshold)
        return "\n".join(p.payload["original_text"] for p in points)
```

> [!danger] Bugs in the book's version, and what each one breaks
> | Book code | What breaks |
> |---|---|
> | `create_collection` **deletes and recreates** if the collection exists, and `store_file_content_in_db` calls it on every upload | **Each upload wipes the entire knowledge base.** Only the last PDF survives. |
> | `id=response.count` | Two uploads at once read the same count → same ID → one silently overwrites the other. Use `uuid4()`. |
> | One `upsert` per chunk | One network round trip per 512 characters. Batching is much faster. |
> | `query_points(query_vector=...)` | Wrong keyword. Current `qdrant-client` takes `query=` (checked against the Qdrant client docs). |
> | `class VectorService(VectorRepository)` | Inheritance glues the service to Qdrant. Composition (`self.repo`) keeps them swappable and testable. |
> | `filepath.replace("pdf", "txt")` | Replaces **every** "pdf" in the path (`pdfs/x.pdf` → `txts/x.txt`). Use `Path(p).with_suffix(".txt")`. |

**What to steal:** the split itself, plus "store the original text in the payload." An embedding can't be turned back into text, so you have to keep the text alongside the vector.

---

## 7. One shared client per app, created in `lifespan`

The book creates a module-level singleton (`vector_service = VectorService()`), and Ex 5-16 opens a **new** `aiohttp.ClientSession()` for every LLM call. Both work in a demo. The production version creates clients once at startup, closes them at shutdown, and injects them where needed:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    qdrant = AsyncQdrantClient(host="localhost", port=6333)
    app.state.vectors = VectorService(VectorRepository(qdrant))
    app.state.http = httpx.AsyncClient(timeout=30)
    yield
    await app.state.http.aclose()
    await qdrant.close()

app = FastAPI(lifespan=lifespan)

def get_vectors(request: Request) -> VectorService:
    return request.app.state.vectors

# in a handler:  vectors: VectorService = Depends(get_vectors)
# in tests:      app.dependency_overrides[get_vectors] = lambda: FakeVectors()
```

**Why:** connection pooling is reused instead of rebuilt on every request, shutdown is clean, and you can swap a fake in for tests with one line.

---

## 8. Background tasks: mixing sync and async steps (Ex 5-13, 5-18)

```python
@app.post("/upload")
async def upload(file: UploadFile, bg: BackgroundTasks):
    path = await save_file(file)
    bg.add_task(pdf_text_extractor, path)               # sync → FastAPI runs it in thread pool
    bg.add_task(vector_service.ingest_file, txt_path)    # async → runs on event loop
    return {"message": "Uploaded, processing in background"}   # user gets this immediately
```

**What to steal:** answer the user right away and do the slow work afterwards. Tasks run **in order**, so step 2 can safely depend on step 1's output file.

> [!warning] Know the limits
> - A heavy **sync** task gets a thread. A heavy **async** task that blocks (like `embed()` without `to_thread`) still freezes the server.
> - No retries, no persistence. If the server restarts, queued tasks are gone, and the user never finds out that the work failed.
> - Once you need status polling, retries, or multiple workers, move to a real queue (Celery/ARQ/RQ + Redis).

---

## 9. Treat self-hosted models as just another API (Ex 5-15 to 5-17)

The biggest architecture lesson in the chapter: **don't load the model inside your FastAPI process.** Run it in a dedicated server (vLLM, TGI, Ray Serve). That turns CPU/GPU-heavy inference into ordinary I/O for your API.

The book hand-rolls an `aiohttp` POST to vLLM. Since vLLM speaks the OpenAI protocol, there's a simpler option: reuse the official async client and only change `base_url`.

```python
from openai import AsyncOpenAI

llm = AsyncOpenAI(base_url="http://localhost:8000/v1", api_key=os.environ["VLLM_API_KEY"])

async def generate_text(prompt: str, temperature: float = 0.7) -> str:
    resp = await llm.chat.completions.create(
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        messages=[{"role": "system", "content": "You are an AI assistant"},
                  {"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return resp.choices[0].message.content
```

**Why:** the same code works with OpenAI, vLLM, Ollama, LM Studio, or Groq. Switching providers means changing `base_url`, not the code. You also get built-in retries and typed responses for free.

---

## 10. Retry with exponential backoff (mentioned, not shown)

The book says to throttle external API calls and names `stamina`, but doesn't show the code. Here's a minimal version:

```python
import stamina, httpx

@stamina.retry(on=httpx.HTTPError, attempts=4)   # waits longer after each failure, with jitter
async def call_provider(client: httpx.AsyncClient, payload: dict) -> dict:
    r = await client.post("/v1/chat/completions", json=payload)
    r.raise_for_status()                           # 429/5xx → raises → retried
    return r.json()
```

Combine it with the `Semaphore` from pattern 2: the semaphore caps how many calls run at once, and the retry handles the ones that still get rate-limited.

---

## Quick recall

| Need                                  | Pattern                                                         |
| ------------------------------------- | --------------------------------------------------------------- |
| Sync lib inside async handler         | `await asyncio.to_thread(fn, ...)`                              |
| N concurrent calls, tolerate failures | `gather(..., return_exceptions=True)` + `Semaphore`             |
| Add context to an LLM prompt          | One `Depends()` per source, fail soft with `""`                 |
| Big file in / out                     | `while chunk := await f.read(N)`                                |
| Lazy pipeline                         | `async def` + `yield`, consumed with `async for`                |
| DB access                             | Repository (how) + Service (what), composition, injected client |
| Shared clients                        | Create in `lifespan`, expose via `Depends`, override in tests   |
| Slow work after responding            | `BackgroundTasks`, then a real queue when you need retries      |
| Self-hosted LLM                       | Separate model server + `AsyncOpenAI(base_url=...)`             |
