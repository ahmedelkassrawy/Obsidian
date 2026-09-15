---
date: 2026-09-15
type: audit
tags: [meta, learning-plan, gaps]
description: Per-folder audit of what the vault covers, what is missing, what is weak, and what to write next. Produced by 5 Opus 4.8 review agents reading all 722 notes.
---

# Knowledge Gaps Audit — 2026-09-15

**How this was made:** five review agents each read one area of the vault (all `.md` files, headings + bodies, plus vault-wide greps for concept names). "0 hits" below means the term does not appear anywhere in the vault.

**Headline (proved by reading the notes):**
- The vault is **wide and applied, thin and mathematical**. Most notes answer "what is it / what's the API call". Few answer "why does it work".
- Roughly 60% of the GenAi bulk and most of Problem Solving/Bookmarks are **raw dumps** (pasted code, transcripts, config) with no digestion.
- **Linking is near zero** everywhere. Theory folders (DSA, NLP) never link to practice folders (Problem Solving, GenAi). There is no MOC/index note anywhere.
- **The three biggest holes relative to your day job:** no TypeScript/zod notes at all, no MCP authorization/security notes, no testing notes (`mock` = 0 hits in 148 backend notes).
- `PLAN.md` is 8 raw links and ~6 months stale. It describes a course-watching AI student; the vault describes a working backend/AI engineer.

---

## 1. Ai & ML (108 notes) + DEPI + KOLYA/ml + Data Analysis

### ML / Supervised Learning
**Covered:** Linear/Ridge/Lasso/ElasticNet with cost functions; logistic regression + threshold tuning; KNN; scaling chooser; regression and classification "GoTo" workflow notes; confusion matrix, ROC/AUC, GridSearchCV as snippets.
**Missing (ranked):**
1. Why regularization works: bias-variance math, L1 diamond vs L2 circle picture. "L1 sets weights to zero" is asserted 4 times, never shown.
2. Calibration (Platt, isotonic, reliability diagrams).
3. PR-AUC has no note; ROC/AUC (wrong for imbalance) does.
4. Cross-validation theory: stratified vs group vs time-series splits, nested CV.
5. Multiclass mechanics: softmax derivation, OvR vs OvO, macro/micro/weighted averaging.
6. Naive Bayes (outside DEPI), GLMs, quantile/robust regression.
**Weak:** `1.Confussion Matrix.md` (39 words, pure code). `Hyperparameter Tuning.md` (65 words; `np.arange(0.0001, 1, 10)` is a bug yielding one value). `Logistic Regression.md` stops at "uses sigmoid" (no log-odds, log-loss, MLE).

### ML / Trees & Ensembles (strongest ML cluster)
**Covered:** Tree splitting + full regularization table; bagging vs pasting; OOB; Random Forest + Extra-Trees; AdaBoost weight updates; gradient boosting as residual fitting with manual example; histogram GB; stacking with `cross_val_predict`; ensemble chooser table.
**Missing:**
1. XGBoost internals: second-order Taylor expansion, gain formula with λ/γ, similarity score, sparsity-aware splits. Named ~15 times, never explained. Same for LightGBM (leaf-wise, GOSS, EFB) and CatBoost (ordered target stats).
2. Gini/entropy formulas live only in `DEPI/ML4`, not in the Trees folder.
3. SHAP / permutation importance; MDI cardinality-bias warning missing from `Random Forest.md`.
4. Monotonic constraints, early stopping, `scale_pos_weight`.

### ML / Unsupervised
**Covered:** KMeans (elbow, silhouette, MiniBatch); DBSCAN/HDBSCAN; GMM as soft clustering; PCA with explained variance; t-SNE/UMAP/PCA table; anomaly detection taxonomy + IsolationForest-as-feature trick.
**Missing:** PCA math (covariance, eigendecomposition, SVD route); EM algorithm E/M steps, BIC/AIC; Davies-Bouldin/Calinski-Harabasz/ARI/NMI; hierarchical + spectral clustering (no note); Isolation Forest and LOF mechanisms.
**Weak:** `Clustering.md` is 100% uncommented code; overlaps `KMeans.md` and `Unsupervised Tasks.md` with no links.

### DL / CNN / PyTorch / TensorFlow
**Covered:** Optimizers SGD→Adam→AdamW with decision table; BatchNorm vs LayerNorm; loss table; sklearn Pipeline/ColumnTransformer; learning curves; MLP sizing; conv output-size arithmetic; transfer learning (Keras + PyTorch); PyTorch tensors, loops, Dataset/DataLoader, save/load; autoencoder intro.
**Missing (ranked):**
1. **Backprop by hand** through a 2-layer net. Biggest interview hole.
2. `autograd` mechanics: computation graph, `requires_grad`, why `zero_grad()`, `detach()`, `no_grad` vs `inference_mode`.
3. Weight init (Xavier/He) and why they pair with activations. Absent.
4. Dropout (inverted dropout, train/eval mode).
5. Modern CNNs: ResNet residuals, Inception, EfficientNet, MobileNet. `[[ResNet]]`, `[[VGG]]`, `[[Inception]]` are dead links.
6. GANs and diffusion: note titled "Autoencoders, GANs, and Diffusion" covers only autoencoders. No VAE/reparameterization, no GAN loss, no diffusion forward/reverse.
7. Mixed precision, gradient clipping/accumulation, DDP.
**Weak:** `Metaheuristics and Optimization Algorithms.md` (Arabic slide commentary, unsupported ranking). `Tensorflow.1 DL.md`, `MLP Code.md` snippet dumps. `Ai & ML/Time Series.md` and `ML/Time Series.md` are drifted near-duplicates. `Loss Functions.md` has the same table twice.

### NLP (deepest folder)
**Covered:** BoW/TF-IDF/Word2Vec with worked numbers; tokenization incl. WordPiece; NLTK pipeline; RNN/GRU/LSTM in Keras + PyTorch, packed sequences; seq2seq + attention; beam search; transformers end-to-end; fine-tuning taxonomy (full, head-only, PEFT named, DAPT, SetFit, MLM); BLEU/ROUGE/METEOR/perplexity; semantic search, dense retrieval, reranking.
**Missing:**
1. The attention equation softmax(QKᵀ/√d)V and *why* √d. Q/K/V is explained by analogy only.
2. Tokenizer training algorithms: BPE merge loop, WordPiece criterion, Unigram/SentencePiece.
3. Word2Vec internals: negative sampling, hierarchical softmax; GloVe, FastText.
4. LoRA math: rank decomposition, α/r, QLoRA.
5. KV cache, RoPE/ALiBi, FlashAttention, GQA/MQA.
6. Decoding: temperature, top-k, top-p, repetition penalty.
7. Contrastive sentence embeddings (MNRL, triplet loss).
**Weak:** `LSTM PyTorch.md` (19 words). `Summarization.md` (one pipeline call). `Attention is all you need.md` raw unpunctuated. **`Stanford CS224n.md` is 13.5k words of undigested transcript** — largest unprocessed block in the vault.

### MLOps / Design ML Systems / ML Interviews
**Covered:** MLOps maturity levels, anti-patterns, project structure, ONNX, Docker multi-stage, pytest for models; MLflow tracking/registry; DVC; serving patterns; Chip Huyen ch.1–4, 8; LLMOps stack survey; one Instagram feed-ranking interview writeup.
**Missing:**
1. Feature stores, offline/online parity, **training-serving skew** (the #1 production ML bug, no note).
2. Shadow deploy, canary, A/B, bandits.
3. CI/CD for ML end to end (GitHub Actions: test→train→register→deploy).
4. Chip Huyen ch.5–7 and 9–11 (feature engineering, offline eval with slices, deployment, humans).
5. Latency/throughput: quantization, distillation, ONNX Runtime vs TorchServe vs Triton.
6. Only one ML system design writeup. Search ranking, ads CTR, fraud, moderation absent.
**Weak:** `MLOPS.md` is a LinkedIn link + tool list + TODO. `Design ML System.1` / `Designing ML Systems.1` are two drifted drafts of one chapter.

### Recommender Systems
**Covered:** Content-based, item-item CF, hybrid, 3-stage funnel, two-tower with in-batch negatives, MovieLens + FAISS build, FAISS vs ScaNN.
**Missing:** Matrix factorization math (ALS/SGD, BPR/WARP); ranking models (Wide&Deep, DeepFM, DLRM, DIN); NDCG/MRR/HitRate@K; cold start, popularity bias, diversity/MMR.

### DEPI / KOLYA / Data Analysis
- **DEPI** duplicates `Ai & ML/ML` topic-for-topic but is *better on math* (Gini/entropy by hand, BPTT, attention equations). The two folders never link.
- **KOLYA/ml** has the best math in the vault (vectorized GD, normal equation). Isolated. Missing: why (XᵀX)⁻¹ breaks on collinearity, O(n³) cost.
- **Data Analysis missing:** real pandas depth (groupby/transform, merge pitfalls, MultiIndex, pivot/melt, copy-vs-view, `SettingWithCopyWarning`); statistical testing in practice (t/chi²/ANOVA choice, p-values, multiple comparisons, bootstrap, power); classical time series (ARIMA, stationarity/ADF, ACF/PACF, rolling-origin backtesting). **`LSTMS Forecasting.md` fits MinMaxScaler before the split — data leakage, contradicting the vault's own `Data Leakage.md`.**
- **Weak:** `Pandas Cheatsheet.md` (193 words) duplicated by `Panda Freq Code.md`; Matplotlib 3/4/5/10 pasted scripts.

### Cross-topic gaps (AI & ML)
- `Ai & ML/NLP` ↔ `GenAi/` never touch. `NLP/Tasks/Semantic Search` links `[[Retrieval-Augmented Generation (RAG)]]` — dead link — while RAG notes exist in GenAi.
- `DEPI/ML` ↔ `Ai & ML/ML` duplicated curriculum.
- `Data Leakage` ↔ `Pipelines` ↔ `LSTMS Forecasting`: the rule, the fix, and the violation, unlinked.
- `Recommender Sys` ↔ `Semantic Search` ↔ `FAISS` are one idea in three folders.

---

## 2. GenAi (161 notes) + MiniRAG + Claude Code Learning

**Headline:** strong on agent frameworks and RAG plumbing; weak on model internals, evaluation as engineering, security, serving economics.

### Agents / Agents in Production / Defensive Guide / DeepAgents
**Covered:** ReAct/plan-execute/ToT; context engineering + compaction; prompt caching mechanics; Uber Eats case study; memory via Redis/Mem0; sandboxing (Docker, bwrap); Cloudflare Durable Object agent.
**Missing (ranked):**
1. **Agent evaluation as engineering**: trajectory eval, pass@k, golden-set construction, rubric design, LLM-judge calibration, CI regression gates. `Agent Evaluation.md` is 3.4 KB of slogans. deepeval/promptfoo/braintrust = 0 hits.
2. **Prompt injection & agent security**: indirect injection via tool output, tool poisoning, confused deputy in MCP, least-privilege scoping, HITL as a security control. 4 one-line mentions total.
3. Vendor-neutral agent memory: what to store, write/read policies, decay, episodic vs semantic vs procedural.
4. Cost/latency engineering: token accounting per turn, cache-hit economics, model routing, p95 budgets. 51 scattered asides, no note.
5. Multi-agent failure modes.
**Weak:** `Agents.md`, `Agent Patterns.md` are name lists. `AWS Bedrock Agent Core.md` pasted code. `Sandbox in Agent.md` 5 lines + screenshots.
**Strong (the model to copy):** `System Design for AI Agents (Architecture and the Why).md`, Uber Eats note.

### LangGraph / Langchain / CrewAI / ADK / LlamaIndex / DSPy
**Covered:** LangGraph state/checkpointers/map-reduce/memory; LangChain v1 agents, structured output; 5 multi-agent notes; CrewAI crews vs flows; ADK 67 KB (arch/memory/sessions/A2A/deploy); LlamaIndex RAG; DSPy signatures/optimizers.
**Missing:** a **framework-agnostic agent-loop note** (messages → tool schema → call → append → repeat) and where each framework puts state/retries/interrupts. No OpenAI Agents SDK, AutoGen; Pydantic AI is a 2.8 KB stub.
**Weak/stale:** **13 files still use pre-1.0 LangChain** (`LLMChain`, `initialize_agent`, `RetrievalQA`, `AgentExecutor`) — incl. `RAG/Hyde RAG`, `RAG Hybrid Search & Reranking`, `Sentence Window RAG`, `Langchain Voice Agent`, `PaddleOCR Basics`. They sit next to `Langchain v1.md` and contradict it. ~80% of framework notes are API transcription.

### RAG + MiniRAG
**Covered:** hybrid BM25+dense + RRF, reranking, HyDE, parent-child/sentence-window, contextual retrieval, GraphRAG + Neo4j, Pinecone/PGVector, retrieval metrics, a real POC note with LRU/Redis caching. MiniRAG: Nginx, Celery, RabbitMQ, Prometheus, Grafana, ngrok.
**Missing:**
1. Embedding internals: contrastive training, in-batch negatives, why cosine, Matryoshka, when to fine-tune an embedder.
2. Vector index internals: HNSW layers and `ef_search`/`M`, IVF-PQ, recall-vs-latency, memory per million vectors, **filtered search wrecking ANN recall**.
3. RAG evaluation end to end: labeled query set, retrieval bug vs generation bug.
4. Ingestion at scale: dedup, incremental re-index, delete/update, versioned indexes.
**Weak:** `RAG Cheatsheet.md` = one embedded PDF. Three `Untitled.md`. `Advanced RAG.md` code dump. MiniRAG = config paste (`Redis.md` is 10 env vars).

### LLM (8 notes) — biggest gap in GenAi
**Covered:** KV cache (2 decent notes), prefill vs decode, LLM proxies/LiteLLM/fallbacks.
**Missing (all 0 hits):** attention math, GQA/MQA, RoPE, FlashAttention, PagedAttention, speculative decoding, MoE, why decode is memory-bandwidth-bound, sampling internals, BPE tokenization, logprobs. The two best transformer explanations are buried in `AI Engineering Book/Ch2` and `Buidling GenAI Services Book/Ch3`.

### Finetune / HuggingFace
**Covered:** pretrain/mid/post-train taxonomy, LoRA/QLoRA with real hyperparameters, Axolotl on RunPod, PEFT notebook, HF pipelines.
**Missing:** **DPO has zero real coverage** (all 23 hits are the substring in "endpoint"). No RLHF/PPO/GRPO, reward modeling, preference data, eval vs base, catastrophic forgetting, distillation, serving adapters, "fine-tune vs prompt vs RAG" decision.
**Weak:** `LLM Finetuning & Deployment Notes.md` = a Notion link.

### MCP (5 notes) — most job-relevant
**Covered:** JSON-RPC, tools/resources/prompts, sampling, lifecycle, FastMCP build, a good best-practices/refactor note, stdio vs streamable HTTP.
**Missing:** **OAuth/authorization spec = 0 hits.** Elicitation (0), roots (0), tool annotations `readOnlyHint`/`destructiveHint` (0), resource templates/subscriptions, progress + cancellation, pagination, versioning without breaking clients, **MCP threat model** (tool poisoning, rug-pull, cross-server shadowing), testing whether the model picks the right tool. **TypeScript SDK absent — notes are Python, the job is TypeScript.**

### Voice / Temporal / Cloudflare / OCR / vLLM / Claude Code Learning
**Covered:** Pipecat frames/transports/STT/TTS/turn detection (most complete framework set); Temporal applied to real ingestion (good); Workers watchdog/heartbeat (good); PaddleOCR; Claude Code internals (agent loop, compaction, memory — strong).
**Missing:** voice latency budget (TTFA, barge-in, endpointing) and eval (WER); **vLLM is effectively empty** (`vLLM/Lesson.md` = frontmatter only); no quantization comparison (GPTQ/AWQ/FP8); **`AI Engineering Book/Ch4. Evaluation AI Systems.md` is a 0-byte file**; `Learning/Links.md` unprocessed.

### Cross-topic gaps (GenAi)
- Five frameworks re-teach the same five ideas (state, tool loop, handoff, subagent, checkpoint) in five vocabularies; no unifying note.
- Memory exists in 6 places (LangGraph, ADK ×2, Redis, Mem0, Claude Code), no comparison.
- Evaluation scattered across 5 notes; the consolidating chapter is empty.
- No security layer at all across ~180 notes — dangerous for a write-capable MCP server against Meta's API.

---

## 3. Backend (53) + API (33) + Deployment (7) + Database (40) + SQL (12) + Linux + OS

### Backend
**Covered:** Celery (excellent 1418-line guide + IdempotencyManager race review); SQLAlchemy 15-note 2.0 series (best-written folder in the vault); FastAPI+Pydantic+SQLAlchemy 10-note series; REST principles, validation layers, handlers/services/repos; System Design (caching ×2, concurrency, consistent hashing, RabbitMQ, estimation); Observability Pt.1; TLS handshake; OSTEP 1–2; Git.
**Missing (ranked):**
1. **Testing — near zero.** `mock` = 0 hits, `fixture` = 1. No fixtures, `TestClient`, DB-per-test, transactional rollback, unit vs integration.
2. **Alembic** — 10 lines inside `Advanced Topics`. Nothing on autogenerate lying, data migrations, live-table migration.
3. **CI/CD** — GitHub Actions in exactly 1 file.
4. Async Python internals: what blocks the loop, `run_in_executor`, cancellation, `TaskGroup`, why `def` endpoints go to a threadpool. GIL never explained.
5. Message-queue patterns: `outbox`, `dead letter`, `circuit breaker`, `backpressure` = 0 hits each.
6. Observability Pt.2: `correlation id` = 0, structured logs, trace propagation, SLOs.
7. Rate limiting (token bucket / sliding window / Redis impl).
8. Design Patterns: only Singleton. No DI, repository, unit-of-work, strategy, adapter — despite using them.
9. Security: `OWASP` = 0, `secrets management` = 0, `12-factor` = 0.
10. Redis as datastore: types, TTL/eviction, pipelines, Lua, cache stampede.
**Weak:** `Tools/Git.md` (superseded by `Git — hands-on reference`); `OSTEP .2 Process.md` (16 lines); `Stack vs Heap.md` (24 lines); `Hands On API/Ch2` (gRPC stub, Ch1 missing); `Deployment/AI Engineering Specific Use Cases.md` copied README.

### API
**Covered:** Pydantic (663 lines), response models, files, webhooks, OAuth2 password flow, MongoDB, RBAC; FastAPI Users 8-part walkthrough; gRPC + protobuf (411 lines); API Gateway; headers vs cookies; JWT.
**Missing (ranked):**
1. OAuth2 flows beyond password: auth code + PKCE (`PKCE` = 0), client credentials. **`FastAPI Users/8. OAuth2.md` is empty — one URL.**
2. JWT pitfalls: `alg: none`, key rotation, **refresh tokens (0 hits)**, revocation, why JWT is bad for sessions.
3. Sessions vs tokens, CSRF (one line).
4. HTTP internals: `ETag` = 0, `HTTP/3` = 0, `Cache-Control` 1 hit, keep-alive, compression, content negotiation.
5. Serving: `gunicorn` = 0. Workers vs threads, graceful shutdown, lifespan.
6. API versioning, pagination contracts, error envelopes.
7. WebSockets / SSE.
**Weak:** `FastAPI - Scheduler.md` (6 lines, `BackgroundScheduler` in async app is a trap it doesn't mention); `FastAPI - Structure.md` unreadable without pasted images; **6 wikilinks across 33 notes.**

### Deployment
**Covered:** Docker walkthrough, EC2 + compose runbook, K8s concepts (pods/deployments/services/Helm), Azure + GitHub Actions, HF Spaces, React+.NET.
**Missing:** Docker internals (`layer cache` = 0; multi-stage, `.dockerignore`, non-root, healthchecks); Compose properly (networks, depends_on vs healthcheck, volumes); **launchd = 0 hits although you run 4 launchd jobs in production**; Cloudflare Workers deploy = 0 notes; reverse proxy/TLS termination; K8s ConfigMaps/Secrets/limits/probes ("Core Concept #6, #7" never written); zero-downtime/rollback/blue-green/feature flags = 0.
**Weak:** `Docker.md` verbatim docker.com tutorial. Azure/HF/React notes are click-paths. **0 wikilinks in the folder.**

### Database (strongest domain in the vault)
**Covered:** Indexing 7 notes (scan types, EXPLAIN ANALYZE, covering/INCLUDE, leftmost rule, bloom, CONCURRENTLY); 2PL, S/X locks, `SELECT FOR UPDATE`, keyset paging; replication single/multi-leader; InnoDB/MyISAM/SQLite; CAP/BASE, Memcached, MongoDB ×3; Postgres wire protocol via Wireshark, SSL; High Performance MySQL incl. MVCC + isolation; pooling best practices.
**Missing (ranked):**
1. **Postgres MVCC / vacuum** — MVCC explained for InnoDB only. xmin/xmax, dead tuples, autovacuum, bloat, XID wraparound: `vacuum` = 1 hit.
2. Isolation levels as one note (4 levels × 3 anomalies with runnable demos).
3. Index types beyond B-tree: GIN, GiST, BRIN, hash, partial, expression.
4. **SQLite specifics**: WAL mode, `busy_timeout`, writer locking, PRAGMA tuning — absent (you ship SQLite).
5. `pgbouncer` = 0; `Section8/Pooling.md` is **empty**.
6. Transactions from the app: savepoints, retry-on-serialization-failure with SQLAlchemy sessions.
7. `Sharding.md` = 19 lines of docker commands.
8. Schema migrations at scale (NOT NULL on a hot table, online DDL, backfills).
**Weak:** `Indexes Concurrently.md` (5 lines); `Database/SQL/SQL.md` 685 lines with **zero headings**, duplicates `SQL/`.

### SQL
**Covered:** T-SQL course — DDL/DML, joins, CTEs, window functions, procs, triggers, cursors, MERGE, XML; 1700-line one-page summary.
**Missing:** this is **SQL Server**, not the Postgres/SQLite you ship. `RETURNING`, `ON CONFLICT`, JSONB, `LATERAL`, `GENERATED`, recursive CTEs for trees, reading a Postgres plan (lives in Database/, unlinked).

### Linux + OS (thinnest relative to need)
**Covered:** basic commands ×3 (redundant), permissions Q&A, user management; OSTEP ch.1–2, stack vs heap.
**Missing:** processes/signals (SIGTERM vs SIGKILL, zombies, exit codes, `nohup`); **service management (`launchd` = 0, `systemd` = 1)**; network debugging (`tcpdump` = 0, `lsof -i`, `dig`, `curl -v`); filesystem/disk (`df`/`du`/inodes/symlinks); env vars, PATH, shell startup, `set -euo pipefail`; `journalctl`, logrotate. OS: scheduling, virtual memory/paging, filesystems, context-switch cost, mutex/semaphore/condvar.
**Weak:** `Linux Commands.md`, `Shell.1.md`, `Bash Shell and Commands.md` are the same list at 3 depths. `KOLYA/OS/Untitled.md` untitled homework.

### Cross-topic gaps (Backend)
- Three SQL silos (`SQL/`, `Database/SQL/SQL.md`, `Database/Indexing`), no links.
- API/ is orphaned; 4 auth notes never reference each other.
- SQLAlchemy N+1 ↔ Database EXPLAIN never connected.
- Concurrency split 4 ways (System Design, DB locks, asyncio, OSTEP), zero links.
- Celery ↔ RabbitMQ ↔ Idempotency are one story in three notes.
- `Deployment/` and `Backend/Deployment/` are two folders with overlapping Docker content.

---

## 4. DSA (18) + Problem Solving (126) + STL (15) + CPP (18) + OOP (5)

### Problem Solving (strongest folder here)
**Covered:** `PS Level 1` is genuinely digested — Graphs/DFS (4.5k words), BFS applications (4.1k), Sliding Window (3.1k, teaches when NOT to use it), Recursion, Backtracking, Bitmasks, Binary Search, Two Pointers, prefix/difference arrays, Number Theory ×2, DP ×2. `ECPC Reference Sheet.md` 13 sections + "which technique?" table.
Solutions in `Bookmarks`: BFS 16, DP 16, Graph 15, DP Iterative 11, Arrays 8, Backtracking 8, Binary Search 7, String 7, Math 5, STL 4, Freq Array 2, Structs 2, Bitmask 1, Geometry 1, Two Pointers 1.
**Missing:** string algorithms entirely (**KMP, Z, hashing, trie, suffix array = 0 hits**); segment tree / Fenwick (deferred to "Level 2"); DSU beyond a 20-line snippet; Bellman-Ford, Floyd-Warshall, SCC, MST, 0-1 BFS; monotonic stack/queue; meet-in-the-middle; interval/bitmask/digit/tree DP; CRT; greedy exchange-argument proofs.
**Weak:** the 104 Bookmarks notes are a pile — 11 have zero prose, ~90 have 1–5 lines (usually just the vjudge link). Filenames are contest letters (`DP -- Z.md`, `Graph T -- ICPC Mansoura.md`), unsearchable. **No pattern index note links technique → solved problems.**

### DSA (weakest theory folder)
**Covered:** Recursion, BST, arrays/subarrays, bits, deque, quick/insertion/selection sort, greedy (set-cover), binary search, BFS intro, Dijkstra, DP, KNN.
**Missing (ranked):** complexity analysis proper (`Intro to Algos.md` = 69 words; no Big-O/Θ/Ω, recurrences, Master theorem, **amortized analysis**); heaps (no note; `STL/Priority Queue` is API only); hash table internals (194-word stub, no buckets/collisions/load factor); merge sort = 0 hits; balanced BSTs (AVL/red-black/rotations); DSU/segment tree/Fenwick/trie; graph algos beyond BFS/Dijkstra.
**Weak:** **`Dijkstra's algorithm.md` contains a factual error** ("only works on graphs with no cycles" — the real constraint is non-negative weights; the note contradicts itself). `Dynamic_Programming_Notes.md` is **empty**. `Dynamic Programming.md` is Arabizi note-to-self.

### STL
**Covered:** vector (with growth), map/unordered_map, set, pair, stack, queue, deque, priority_queue, linked list (3.5k words, best note), frequency array, prefix sum, sliding window, hash tables.
**Missing:** iterator categories; `<algorithm>` beyond sort (`accumulate`, `next_permutation`, `nth_element`, `unique+erase`); custom comparators; `multiset`/`multimap`; `std::array`/`span`/`string_view`; anti-hash tests; one container complexity table.
**Weak:** `Unordered Map.md` **empty**. `Sliding Windows.md` and `Prefix Sum.md` superseded by PS Level 1 notes, no link.

### CPP (biggest gap for a backend engineer)
**Covered:** functions, overloading, references, pointers (90 words), structs, classes, constructors, templates (217 words), namespaces, headers, forward decl, linkage (1.6k words, best note), control flow, type conversion, strings.
**Missing (all ~0 hits):** memory model/ownership (`new`/`delete`, leaks, dangling); **RAII**; **smart pointers**; **move semantics / rvalue / rule of 0/3/5**; **undefined behaviour**; **const-correctness**; compilation & linking (translation units, ODR, include guards, static vs dynamic libs); exceptions; lambdas/`std::function`; template specialisation/variadics/concepts.
**Weak:** `Pointers.md`, `Strings.md`, `Structs.md`, `Classes.md`, `C++.md` are all under 100 words. `CPP/OOP.md` duplicates `OOP/`.

### OOP
**Covered:** association/aggregation/composition, inheritance ×2, polymorphism, static members, operator overloading, enums, structs vs class, boxing/unboxing.
**Missing:** SOLID (0 hits); design patterns (0 hits); "prefer composition" argument; interfaces/abstract/pure virtual; **vtables** (0 hits); virtual destructors; diamond problem; `override`/`final`.
**Weak / wrong language:** **all five OOP notes are C#** (25 C# fences; `OOP.5` covers CLR boxing which does not exist in C++). Files named `OOP.1`–`OOP.5`, unfindable by topic.

### Cross-topic gaps (DSA)
- Theory and practice never touch: `DSA/BFS.md` (153 words) doesn't link to 16 BFS solutions or the 4.1k-word PS note. Same for Binary Search (3 competing notes), Recursion, Prefix Sum, Backtracking, DP.
- 21 wikilinks in 18 DSA notes, 6 in 15 STL, 3 in 5 OOP. No MOC.
- Reference sheet duplicates PS Level 1 section-for-section with no links.
- `Excalidraw/URL Shortener` is the only system-design drawing and links to nothing.

---

## 5. Python (29) + JS (2) + Interviews (12) + ALX (3) + Clippings (11) + PLAN.md

### Python
**Covered:** Recent good notes (Aug 2026): `Data Modeling`, `Pydantic`, `Protocol vs ABC`, `Decorators`, `JSON Serialization`, `Testing with pytest` — worked examples from the `postqueue` project. Basics from a Jul 2026 course. Numpy 6 tiny notes, Pandas 9 cheat-sheet notes.
**Missing (0 hits each):** iterators & generators (`yield` appears nowhere); dunder methods beyond `__init__`; context managers (class form, `ExitStack`); closures named; asyncio in Python/ (exists in `API/Concurrency and Async.md`, misfiled, no event-loop internals/`TaskGroup`/cancellation); **GIL, threading vs multiprocessing (already cost you an InstaBug question)**; typing generics/`TypeVar`/`TypedDict`/`Literal`/`overload`; dataclasses (and "dataclass vs pydantic vs NamedTuple"); pytest `fixture`/`parametrize`/`monkeypatch`/`mock` (note stops at `assert` + `pytest.raises`); packaging (`pyproject`, uv, conda); stdlib (`itertools`, `functools`, `pathlib`, `collections`, `enum`); logging; profiling; memory model (refcount, GC, mutable defaults); metaclasses/descriptors; error-handling patterns; walrus/`match`.
**Weak:** all 6 Numpy notes and most Pandas notes are pasted code. `Pandas.7 Sorting.md` = 109 bytes. `Counter.md`, `Reading & Writing.md`, `Exceptions.md` stubs. `OOP.md`/`Data Structures.md`/`Python Review.md` overlap.

### JS / TypeScript — biggest hole in the whole vault
**Covered:** `Fundamentals.md` (15 KB, decent JS basics), `Untitled.md` (2 KB).
**Missing:** **not one TypeScript note** although you ship TS MCP servers. Types vs interfaces, generics, unions/narrowing, utility types, `unknown` vs `any`, `strict`, `tsconfig`; **zod** (the MCP SDK schema layer — nothing); event loop, microtask vs macrotask, promises, async error handling; prototypes/`this`/classes; ESM vs CJS, `exports`, dual builds; Node streams/`Buffer`/**stdio transports (MCP runs on stdio)**; npm/pnpm, semver, lockfiles, vitest, eslint.

### Interviews
**Covered:** Orange (7 notes, strong MLOps/drift/K8s/SageMaker); InstaBug (2: ULID vs UUID, race conditions, webhooks, index lookups); Vodafone (logistics + STAR script). Eventum = 91-byte link.
**Missing:** no cross-company **question bank by topic**; no **post-mortem** (outcomes, fumbled questions); no interview-oriented system design note; not linked to Problem Solving; take-home strategy; salary negotiation for the Egyptian market; reusable STAR library. InstaBug Q&A starts at Q8 (Q1–Q7 missing).

### ALX
Three prompt dumps (job boards, career-coach prompts, "what is an LLM"). No resume, cover letter, or outcome. Dead weight unless completed artifacts are added.

### Clippings (940 KB, 9 of 11 undigested)
**Worth digesting, in order:** `11. Complete REST API Design` (107 KB) → 2-page checklist; `3- Caching Strategies` (117 KB) → cache-aside/write-through/write-behind table; `10. Controllers, services, repositories` (57 KB) → layering note; `OBSERVABILITY FROM SCRATCH` (140 KB) → logs/metrics/traces (you have no logging note); `9. Validations` → merge into `Pydantic.md`. The rest (fine-tuning transcript, Fowler case study, self-attention) duplicate existing notes — link or delete.

### Plan vs reality
`PLAN.md` = 8 raw links, no dates/goals/progress. `README.md` = one line.
- Planned, has notes: CS224n, LLM fine-tuning.
- Planned, no notes: Manara tree, DeepLearning.AI post-training/RL course (no RLHF/DPO/GRPO anywhere), Agentic AI + Multimodal RAG courses.
- Has notes, not in plan: nearly everything you actually did (Backend, Celery, FastAPI, MCP, LangGraph, MLOps, PyTorch, the August Python revival).

---

## Consolidated Top 15 — what to write next, ranked by job impact

1. **TypeScript + zod for MCP servers** — you ship this daily, zero notes.
2. **MCP authorization + threat model** — OAuth 2.1, tool annotations, elicitation, tool poisoning, confused deputy. Zero coverage, write-capable server against Meta's API.
3. **Testing**: pytest fixtures/parametrize/monkeypatch/mock + FastAPI `TestClient` + transactional test DB. `mock` = 0 hits vault-wide.
4. **Prompt injection & agent security** — indirect injection via tool results, least privilege, HITL as a control.
5. **Evaluation harness end to end** — fill the 0-byte `AI Engineering Book/Ch4`: golden sets, LLM-judge calibration, trajectory eval, CI gates.
6. **Transformer internals** — attention equation + why √d, GQA, RoPE, KV cache, why decode is memory-bound. Fixes both NLP and GenAi/LLM at once.
7. **Backprop by hand + PyTorch autograd semantics** — the most-asked DL interview question and the reason your training loops are copied, not understood.
8. **Async Python internals + GIL + threading vs multiprocessing** — already cost an InstaBug question.
9. **Postgres MVCC/vacuum + SQLite WAL/locking** — you ship both; your only MVCC note is InnoDB.
10. **Alembic in practice + CI/CD pipeline anatomy** — 25 SQLAlchemy notes, 10 lines on changing a schema safely, 1 mention of GitHub Actions.
11. **Linux/ops note: processes, signals, launchd/systemd, ports, logs** — 4 launchd jobs in production, `launchd` = 0 hits.
12. **XGBoost/LightGBM/CatBoost internals** — recommended constantly, never explained.
13. **C++ memory: RAII, smart pointers, move semantics, rule of 0/3/5, UB, const** — all 0 hits.
14. **Complexity & amortized analysis + heaps + hash table internals** — every interview opens here; current notes are 69–194 words.
15. **Problem Solving pattern index** — one note mapping technique → the 104 solutions; rename contest-letter files to problem names.

## Cheap housekeeping (under an hour total)
- Delete/merge empty files: `DSA/Dynamic_Programming_Notes.md`, `STL/Unordered Map.md`, `Database/.../Section8/Pooling.md`, `FastAPI Users/8. OAuth2.md`, `vLLM/Lesson.md`, `AI Engineering Book/Ch4`, three `Untitled.md` in GenAi, `RAG Cheatsheet.md`, `Pandas.7 Sorting.md`, `Interviews/Eventum.md`, `Backend/Tools/Git.md`.
- Fix the factual errors: `DSA/Dijkstra's algorithm.md` (cycles claim), `ML/Hyperparameter Tuning.md` (`np.arange` bug), `LSTMS Forecasting.md` (scaler fit before split).
- Stamp `> stale — pre-LangChain-1.0` on the 13 old-API notes.
- Merge duplicate pairs: Linux command notes ×3, `Time Series.md` ×2, `Design ML System.1`/`Designing ML Systems.1`, `Pandas Cheatsheet`/`Panda Freq Code`, STL vs PS Level 1 Sliding Window / Prefix Sum, `CPP/OOP.md` vs `OOP/`.
- Add headings to `Database/SQL/SQL.md`; title `JS/Untitled.md`.
- Rewrite `PLAN.md` as a dated plan from this list; make `README.md` a vault map with MOC links per folder.

---

## AI Engineer lens (added 2026-09-15) — the ranking that matters

An AI Engineer is judged on four things: (1) can you reason about the model, (2) can you build reliable systems around it, (3) can you prove it works, (4) can you ship it cheaply and safely. The vault is strong on (2)'s plumbing and weak on the other three. Ranked by what most blocks you being a *senior* AI Engineer rather than a framework user.

### Tier 1 — you cannot call yourself an AI Engineer without these (all currently ~0 coverage)
1. **Transformer internals** — attention equation, why √d, multi-head → GQA/MQA, RoPE, KV cache, why decode is memory-bound. Every latency/cost/context question reduces to this.
2. **Evaluation as engineering** — golden sets, LLM-judge calibration, trajectory eval for agents, RAG retrieval-vs-generation bug triage, CI regression gates. `AI Engineering Book/Ch4` is 0 bytes. Nothing you build is trustworthy without this.
3. **Prompt injection & agent security** — indirect injection via tool results, tool poisoning, least-privilege tools, HITL as a security control, MCP threat model + OAuth. You run a write-capable agent against Meta's API today.
4. **Embeddings + vector index internals** — contrastive training, Matryoshka, HNSW `ef`/`M`, IVF-PQ, filtered-search recall collapse, when to fine-tune the embedder. You run RAG in prod and know only the API.
5. **Post-training methods** — SFT vs DPO vs RLHF/GRPO mechanics, preference data, reward models, "fine-tune vs prompt vs RAG" decision. DPO = 0 real hits.

### Tier 2 — what separates senior from mid
6. **Cost & latency engineering** — token accounting per turn, cache-hit economics, model routing (small→large), batching, p95 budgets. 51 asides, no note.
7. **Serving** — vLLM/PagedAttention, continuous batching, quantization (GPTQ/AWQ/FP8) trade-offs, speculative decoding, benchmarking. `vLLM/Lesson.md` is empty.
8. **The framework-agnostic agent loop** — one note that explains state, tool loop, handoff, interrupt, checkpoint, memory once, then maps LangGraph/ADK/CrewAI/DeepAgents onto it. Lets you pick tools instead of being picked by them.
9. **Tokenization** — BPE merge loop, WordPiece, SentencePiece; why token counts differ across models and languages (Arabic matters for your clients).
10. **Backprop by hand + autograd semantics** — the floor for any DL conversation and the most common interview opener.
11. **Agent memory design** — vendor-neutral: what to store, write/read policy, decay, episodic vs semantic vs procedural, how it differs from RAG.
12. **Observability for LLM systems** — structured logs with correlation IDs, trace propagation across agent→tool→model, cost per trace. Bridges Backend/Observability Pt.1 with GenAi.

### Tier 3 — engineering foundations an AI Engineer still needs
13. **TypeScript + zod** — your MCP servers are TS; zero notes.
14. **Testing** — pytest fixtures/mock, FastAPI TestClient, plus how to test non-deterministic model outputs (snapshot + tolerance + eval sets).
15. **Async Python + GIL** — inference clients, streaming, concurrency of tool calls.
16. **ML fundamentals depth** — XGBoost internals, calibration, PR-AUC, CV theory, training-serving skew. Still asked in AI Engineer interviews; still used for tabular tasks.
17. **Docker layers/multi-stage + CI/CD** — shipping the model/agent, not just writing it.

### What to deprioritize for this goal
- T-SQL course notes, React+.NET deployment, C# OOP notes, competitive-programming Level-2 structures (segment tree, Fenwick, string algos): keep, but they don't move the AI Engineer needle.
- More framework tutorials (another LangGraph/ADK note): the vault already has too many relative to concept notes.

### Suggested order (one note per week, each linked into a new `AI Engineering MOC.md`)
Week 1 Transformer internals → 2 Tokenization + embeddings → 3 Vector index internals → 4 Evaluation harness → 5 Prompt injection + MCP auth → 6 Agent loop (framework-agnostic) → 7 Cost/latency → 8 Serving/quantization → 9 Post-training (SFT/DPO/GRPO) → 10 Agent memory → 11 LLM observability → 12 Backprop + autograd.
