---
title: "AI Engineering (Chip Huyen) — Ch.3 Evaluation Methodology"
type: reading-note
tags: [ai-engineering, evals, m1]
source: "AI Engineering — Chip Huyen, Ch.3"
date: 2026-08-20
---
# Ch.3: Evaluation Methodology

> Read for M1. The exact-vs-subjective, functional-correctness, and AI-as-judge sections below are the eval harness I'm building this week ([[m1-rag-evals-weekly]]).
>
> The entropy/perplexity section is background: good to know, not what I'll use for RAG. Jump to section 5 for how it maps to the harness.

---

## 1. Why evaluation is its own hard problem

Evaluation isn't a side task. It has to be considered as part of the whole system, not in isolation.

The job of evals: mitigate risk and uncover opportunities. The method: find where the system is likely to fail, then design evals around those spots. Sometimes you have to redesign the system to make failures visible in the first place.

Why foundation models are especially hard to evaluate, three reasons:

1. The smarter the model, the harder to judge. Anyone can tell a first-grader's math is wrong; few can check a PhD-level proof. A gibberish summary is obviously bad, but a coherent summary that's subtly wrong? You'd have to read the book to catch it. Fluent ≠ correct.

2. Output is open-ended. Classic ML was easy: check whether the predicted category matches the expected one. Open-ended text has no single right answer to match against.

3. The model is a black box. You only see input and output, not the reasoning that produced it.

---

## 2. Language-modeling metrics (the entropy family)

> Background, optional for RAG. These measure how well a model predicts text. Useful mental model, but I won't compute them in my RAG eval harness. Skim and move on.

Entropy: average information per token.

- Higher entropy = each token carries more info = more bits to represent it = harder to predict what comes next.

Cross-entropy: how hard it is for this specific model to predict this specific dataset. It depends on two things:

- how predictable the data itself is, and

- how far the model's learned distribution is from the true distribution of the data.

Bits-per-character / bits-per-byte: a fairness fix. Cross-entropy is measured per token, but different models tokenize differently, so we normalize to bits per character or per byte to compare models fairly regardless of tokenizer. (Correction to my first pass: I'd written this as "per token". The whole point of BPC/BPB is to get off tokens so you can compare across tokenizers.)

Perplexity: the model's uncertainty when predicting the next token.

- Intuition: how many equally-likely options it's effectively choosing between. Higher uncertainty means more possible next tokens.

- Perplexity = exp(cross-entropy). Same quantity, different units. (This relationship wasn't in my first pass; it's the anchor that ties the two together.)

- Lower for structured or predictable data (easier to guess).

- Higher for a bigger vocabulary (more possible tokens).

- Lower for longer context (more to go on, so easier to predict).

- Lowest for text the model memorized in training, so perplexity can detect whether a text was in the training data (contamination check).

---

## 3. Two families of evaluation: exact vs subjective

The key split of the chapter.

- Exact: judgment with no ambiguity.

- Subjective: needs interpretation, such as asking an AI to grade quality.

### 3a. Exact evaluation

Functional correctness: evaluate the system on whether it actually performs the intended job, for example whether generated code passes the tests. The gold standard when you can define it.

Comparing an output against reference answers, four ways from strictest to most flexible:

1. Human or evaluator judgment: a person decides "are these two texts the same?"

2. Exact match: the output matches a reference response exactly.

3. Lexical similarity: how similar the output looks to the reference (surface or word overlap).

4. Semantic similarity: how close the output is to the reference in meaning.

Strict and cheap (2, 3) at the top; flexible and fuzzy (4) at the bottom. Reach for the strict one first; use semantic only when meaning can't be pinned to words. (The lesson from my Wednesday eval-harness session.)

### 3b. Embeddings: how "semantic similarity" actually works

- A model turns text into a numerical representation, a vector, that captures meaning. That vector is an embedding.

- An embedding algorithm is good if more-similar meanings land closer together, measured by cosine similarity.

- Example: "the cat sits on a mat" should embed closer to "the dog plays on the grass" than to "AI research is super fun", because the first two are about a similar kind of thing even though the words differ.

---

## 4. AI as a judge (subjective evaluation)

Why use it:

- Fast, cheap, and easy compared to human evaluators.

- Works without reference data.

- Can judge on any criteria: correctness, repetitiveness, toxicity, hallucination, and more.

- It can explain its decision, which helps when you want to audit your eval results.

Because a model is "an aggregation of the masses", its judgments tend to reflect the mainstream view. With the right prompt on the right model, you get reasonably good judgments across many topics.

Tools with built-in criteria:

- Ragas: faithfulness, answer relevance.

- LangChain: Criteria Evaluation.

- Azure AI Studio and MLflow.metrics: groundedness, relevance, coherence, fluency, similarity.

Limits of AI-as-judge (know these cold):

- Inconsistency: the judge is itself non-deterministic; it can grade the same output differently across runs.

- Criteria ambiguity: "is this good?" is under-specified, and vague criteria give noisy scores.

- Cost and latency: every eval is now an extra model call.

- Bias: the judge carries the model's biases into your scores.

---

## 5. How this maps to my M1 eval harness

The chapter is a menu of eval methods. Here's which one each part of my harness is:

| My harness | Huyen's method |
|---|---|
| Layer 1, retrieval hit@k (did the right chunk come back?) | Functional correctness, exact. No LLM in the loop |
| Layer 2, `"2019" in answer` (cheap-strict fact check) | Exact or lexical match on a pinned fact |
| Layer 2, citation check (expected filename is in sources) | Exact match on a reference |
| Layer 2, faithfulness or paraphrase (week 3) | Semantic similarity plus AI-as-judge. Remember the limits above and spot-check the judge |

Takeaways I'm carrying into the build:

- Prefer exact or functional checks wherever I can define them (Layer 1, pinned facts). They're the reliable core.

- Treat AI-as-judge as the last resort, only where meaning can't be pinned to words, and never trust it blind. Inconsistency and bias mean I have to spot-check the judge against my own labels. That's the week-3 "how do I know my judge is any good" gap.

- "Design evals around where the system fails" means my eval set should target rag-prod's real weak spots, like the no-inline, file-level-only citations finding, not generic questions.
