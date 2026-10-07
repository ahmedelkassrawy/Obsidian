---
date: 2026-10-07
type: project-note
project: resolveflow
status: active
tags:
  - domain/ai-eng
  - type/project-note
  - resolveflow
  - topic/rag
description: "Plan for policy RAG in ResolveFlow: why, tenant isolation, document updates, failure handling, indexing, splitting, and PDFs."
hubs:
  - "[[00 ResolveFlow Index]]"
---

# 10 Policy RAG

My first idea:
Each tenant has an id, each tenant has the document and chunked
So we have to ingest first the pdf or the file into the correct tenant and then chunk them using the Recusrive char splitter and then these chunks everyone takes an id and has the metadata of the source which is the document id and then embed them using the embedder 
SO after that we can do the indexing based on the chunks id 
and the hybrid bm25+cosine simliarity and then reranking them and using the redis semantic caching -> for the agent and the rag 

Well strcutured with claude:
why RAG ?
- we need to know if the refund policy allow refunding this duplicate charge 
- answer billing questions

for the duplicate charge we will take the chunks and turn them into Evidence
for the answer billing question we can return them as chunks in the context for the ai to use 
- the answer cites the chunks it used (`chunk_id`), so a reviewer can check it

ingestion + search and getting the correct tenant document is required
- the contract: `search(tenant_id, query, limit)` with `tenant_id` **required**, never an optional filter
- the tenant filter applies to **every** search: the vector search, the BM25 search, the reranker input, and the cache key
- filter by tenant first, then rank

Semantic cache returns a stored answer when a similar question so we have to:
- include the tenant id in the cache key 
- and sits only for answers of the question that are not related to the billing refunds and trasactions
- clear that tenant's cache when one of their documents is replaced, or it keeps serving answers built from the old policy

Future updates to the documents 
what will we do if the docs got updated that would change all the chunks we have 
- a tenant has **many** documents (refund policy, billing FAQ, shipping policy), each with its own `document_id`
- the tenant says which document an upload is: `PUT /documents/{document_id}`. Never guess it from the file name or content
- `tenant_id` comes from the logged-in caller, never from the file or request body
- same `document_id` → **replace**: delete the chunks with that `tenant_id` + `document_id`, insert the new ones, in **one transaction** (a search never sees half a document)
- the tenant's other documents stay untouched
- a `documents` table keeps `tenant_id`, `document_id`, `title`, `version`, `content_hash`, `uploaded_at`
- same content hash as the live version → skip re-ingesting (idempotent upload)
- `Evidence.summary` stores the cited **text**, not just the `chunk_id`, so old tickets still show the rule they relied on after the policy changes

Failure of the search:
- if its related to a refund -> say we dont have a direct policy found and esclaate or handoff to the human
The rule is: answer _only_ from the retrieved chunks, cite them, and when nothing relevant comes back, say "I don't have information on that" or hand off to a human.
- "relevant" needs a cutoff: a minimum similarity score below which a result counts as not found

Why index the embeddings not chunks ids
by id -> you look up by id when we already have the id (for example, showing the text of a citation). The primary key is indexed automatically, nothing to build
we will also have to index the tenant id since each search will use it
by meaning -> we will have take the question and then make it an embedding and searching the embedding itself so thats what makes the index on embeddings that important (HNSW index in pgvector). Without it, every search compares against every chunk

Splitting document based on heading but not every doucment is neatly strucutred so we will use heading when they exists and with a fallback when they dont
	if the section is too long after the split by heading -> we can split with overlap
	- overlap only where we cut **through** text (long sections, or documents without headings), not between heading sections
	- chunk size and overlap are decided by the eval, not guessed

Measure before optimizing
- small eval: ~15 questions → the expected `chunk_id`
- measure: is the right chunk in the top 3?
- add BM25 hybrid or a reranker only if that number is bad

PDFs -> markfown -> split -> embed -> store
- store the converted Markdown next to the original, to see what the parser produced
- scanned PDFs have no text and need OCR
- tools to look at: pymupdf4llm (light), docling (better with tables)