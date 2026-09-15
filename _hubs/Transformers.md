---
description: "Hub: every note about Transformers"
type: hub
domain: ml
tags:
  - type/hub
  - topic/transformers
---
# Transformers

> [!info] Attention, self vs cross attention, the full architecture walkthrough and BERT internals. Strong; the 13k-word CS224n note needs splitting.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/transformers`.

## Concepts
- [[Self-Attention vs Cross-Attention]] — Explains Q/K/V with a library analogy, where self-attention and cross-attention each sit in a transformer, the PyTorch call patterns, and how masking differs between them.
- [[Seq2Seq]] — Explains the encoder-decoder Seq2Seq architecture, the fixed-vector bottleneck problem, how attention fixes it, and how Seq2Seq compares to transformers.
- [[Sparse Vs Dense Embeddings]] — Why sparse vectors waste dimensions and dense ones do not, then the progression from Word2Vec (word meaning) to transformers (context-aware tokens) to SBERT (one vector per sentence).
- [[Stanford CS224n]] — A very long single-file NLP walkthrough from Bag of Words and TF-IDF through embeddings, RNNs and attention to BERT's encoder internals, with formulas and mermaid diagrams.
- [[Tokenizer]] — Compares word-, character- and subword-based tokenization with code for each, plus practice questions on when each breaks down.
- [[Transformers]] — A synthesis note that stitches the transformer story together: why RNNs fell short, how attention fixed it, then embeddings, positional encoding, multi-head attention and the full stack.
- [[Attention is all you need]] `raw` — Running commentary on implementing the Transformer paper: token ids, nn.Embedding to d_model vectors, positional encoding and what each forward pass does.

## How-tos & recipes
- [[Fine-Tuning Tutorial]] — A full fine-tuning tutorial on Rotten Tomatoes sentiment: loading data, BERT setup, freezing layers to save compute, few-shot SetFit, and masked-language-model pretraining.
- [[Modern Tokenization]] — Shows modern subword tokenization with the BERT tokenizer and how to run text through BERT to get contextual embeddings.
- [[Text Classification]] — Four ways to classify text: sentence-transformer embeddings plus logistic regression, zero-shot cosine similarity against label embeddings, and a T5 generative classifier.
- [[Fine-Tuning BERT On MRPC With Trainer]] `raw` — Pasted walkthrough of fine-tuning a model on the GLUE MRPC paraphrase task: loading the dataset, tokenizing, the data collator, and training with the Trainer API.
- [[Hugging Face]] `raw` — Short pasted code for two HuggingFace tasks: text classification with DistilBERT and basic text generation.
- [[NLP Eval Code]] `raw` — Code for computing NLP metrics with the HuggingFace evaluate library: BLEU for translation, ROUGE for summarization and seqeval for NER, wired into a training loop.
- [[Sorting - Sort Three Numbers]] `raw` — Pasted tokenizer code covering encoding text, every padding option, truncation to model max length, and what input_ids and attention masks look like.
- [[Summarization]] `raw` — A minimal HuggingFace summarization pipeline call with bart-large-cnn on a sample passage.

## References & cheat sheets
- [[Fine-Tuning Quick Reference]] — A condensed fine-tuning recipe: add a classification head to a pretrained transformer, tokenize, define metrics, and run the HuggingFace Trainer, plus tricks to improve results.
- [[NLP Evaluation Metrics]] — Explains the evaluation metrics for generative NLP - perplexity, ROUGE variants, BLEU and METEOR - with formulas, examples and when each applies.

## Book notes
- [[Ch2. Understanding Foundation Models]] — Chip Huyen Ch2: the four choices that make models differ - training data, transformer architecture and size, post-training alignment, and sampling (which is why models hallucinate).
- [[Ch3. Serving GenAI Models with FastAPI]] — Ch3 notes: how transformers, tokenization, embeddings and positional encoding work, then how to serve text, image, audio and 3D models from a FastAPI app.
- [[Encoder Vs Decoder Models]] `stub` — Short comparison of encoder models (representation, e.g. BERT) and decoder models (generation) by purpose, input and output.

## Course notes
- [[Seq2Seq And Neural Machine Translation]] — NLP lecture 4: how an RNN language model is trained layer by layer, RNN pros and cons, and the seq2seq encoder-decoder for neural machine translation.

## Clippings (raw)
- [[Clipping - Self-Attention Explained (Article)]] `raw` — Clipped explainer with inline SVG diagrams on self-attention: the context problem, what queries, keys and values are, and how the attention score is computed and combined.

## Related hubs
[[HuggingFace]], [[NLP Preprocessing]], [[Embeddings & Semantic Search]], [[Fine-tuning]], [[RNN & LSTM]], [[LLM Internals]]

## Notes to self (from the audit)
- [[Clipping - Self-Attention Explained (Article)]]: Digest into the NLP/Transformers notes. The SVG diagrams are worth keeping when you rewrite it.
- [[Stanford CS224n]]: Not a raw lecture transcript despite the name - it is a 13.5k-word structured guide with 200+ headings and no CS224n lecture content. Too big for one note: split it per topic and rename.
- [[Attention is all you need]]: Unformatted stream of notes with no headings - worth rewriting as prose with real code blocks.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
