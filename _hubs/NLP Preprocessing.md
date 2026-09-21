---
description: "Hub: every note about NLP Preprocessing"
type: hub
domain: ml
tags:
  - type/hub
  - topic/nlp-preprocessing
---
# NLP Preprocessing

> [!info] Tokenization (word, character, subword), stop words, stemming, lemmatization, padding and modern BERT tokenizers. Strong.
> Part of [[MOC - Machine Learning]]. Also try the tag `#topic/nlp-preprocessing`.

## Concepts
- [[NLP Concepts]] — Compares the main text-representation methods (BoW, TF-IDF, Word2Vec), then BERT vs sentence transformers, and BLEU vs ROUGE for evaluation.
- [[Recurrent Neural Networks (RNNs) and LSTMs]] — Explains what RNNs are for and how their memory works, then the Keras text pipeline (tokenize, pad, embed) and the exact input and output shapes an LSTM layer expects.
- [[Stanford CS224n]] — A very long single-file NLP walkthrough from Bag of Words and TF-IDF through embeddings, RNNs and attention to BERT's encoder internals, with formulas and mermaid diagrams.
- [[Tokenizer]] — Compares word-, character- and subword-based tokenization with code for each, plus practice questions on when each breaks down.

## How-tos & recipes
- [[Modern Tokenization]] — Shows modern subword tokenization with the BERT tokenizer and how to run text through BERT to get contextual embeddings.
- [[NLP]] — An end-to-end NLP guide with code: lowercasing, stop words, tokenization, stemming vs lemmatization, n-grams, feature extraction, model training and saving.
- [[NLP - AI BOOK]] — Shows the Keras text pipeline end to end: Tokenizer to sequences, stop-word removal, padding, an Embedding layer, and a TextVectorization-based classification model.
- [[POS Tagging]] — Builds an RNN part-of-speech tagger in Keras on NLTK corpora: data prep, splits, tokenization, padding, one-hot labels, model, training and inference.
- [[RNN]] — Builds a character and token-level GRU language model from scratch: encoding text to ids, sliding-window datasets, dataloaders, embeddings, and predicting the next character.
- [[RNN and LSTM]] — NLP in PyTorch with RNNs and LSTMs: preprocessing, spaCy tokenization, vocabulary building and numericalization, then an RNN question-answering model and an LSTM next-word predictor.
- [[NLP Preprocess code]] `raw` — Copy-ready NLTK preprocessing block: downloads, tokenizer, stemmer, lemmatizer and a customized stop-word list.
- [[HF Tokenizer - Encoding Padding Truncation]] `raw` — Pasted tokenizer code covering encoding text, every padding option, truncation to model max length, and what input_ids and attention masks look like.

## References & cheat sheets
- [[Fine-Tuning Quick Reference]] — A condensed fine-tuning recipe: add a classification head to a pretrained transformer, tokenize, define metrics, and run the HuggingFace Trainer, plus tricks to improve results.

## Book notes
- [[Text Classification - AI Book]] — Book-chapter notes on text classification: turning a corpus into vectors with CountVectorizer and TfidfVectorizer, then training and scoring a classifier on that matrix.
- [[Word2Vec And Word Embeddings]] `stub` — A paragraph on Word2Vec - predicting a word from its context so that words used alike end up near each other in the embedding space.

## Course notes
- [[NLP Pipeline And Regex Basics]] — NLP lecture 1: the corpus/document/vocabulary vocabulary, the eight-stage NLP pipeline from data acquisition to monitoring, and regex special sequences for text cleaning.
- [[Text Representation - BoW TF-IDF And N-Grams]] — NLP lecture 2: turning text into numbers with Bag of Words, N-grams, TF-IDF and one-hot encoding, worked by hand and then with sklearn vectorizers into a classifier.

## Related hubs
[[Embeddings & Semantic Search]], [[Transformers]], [[RNN & LSTM]], [[HuggingFace]], [[TensorFlow & Keras]], [[Classification]]

## Notes to self (from the audit)
- [[Word2Vec And Word Embeddings]]: 84 words from a book chapter that was never finished.
- [[Stanford CS224n]]: Not a raw lecture transcript despite the name - it is a 13.5k-word structured guide with 200+ headings and no CS224n lecture content. Too big for one note: split it per topic and rename.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
