Corpus -> Paragraph
Document -> Sentences
Vocabulary -> Unique Words

---
# NLP Pipeline

## 1. Data Acquisition
- Gathering raw text data from various sources (e.g., web scraping, APIs, databases, files).

## 2. Text Cleaning and Extraction
- Removing noise, unwanted characters, HTML tags, and extracting relevant text content.

## 3. Preprocessing
- **Tokenization:** Splitting text into words or sentences.
- **Lowercasing:** Converting all text to lowercase.
- **Stop Word Removal:** Removing common words (e.g., "the", "is").
- **Stemming / Lemmatization:** Reducing words to their root form.
- **POS Tagging:** Identifying parts of speech.
- **NER (Named Entity Recognition):** Identifying entities like names, dates, locations.

## 4. Text Representations
- Converting cleaned text into numerical format for ML models.
- **Techniques include:**
    - Bag of Words (BoW)
    - TF-IDF
    - Word Embeddings (Word2Vec, GloVe)
    - Contextual Embeddings (BERT, GPT)

## 5. ML Model
- Training or applying machine learning/deep learning models.
- **Common tasks:**
    - Text Classification
    - Sentiment Analysis
    - Machine Translation
    - Question Answering
    - Text Summarization

## 6. Evaluation
- Measuring model performance using appropriate metrics.
- **Metrics:**
    - Accuracy, Precision, Recall, F1-Score
    - BLEU / ROUGE (for text generation)
    - Perplexity

## 7. Deployment
- Integrating the trained model into a production environment.
- **Options:**
    - REST API (Flask, FastAPI)
    - Cloud Services (AWS, GCP, Azure)
    - On-device deployment

## 8. Monitor & Update
- Continuously tracking model performance in production.
- Retraining or fine-tuning the model as data drifts or requirements change.
---
# Special Sequences

| Sequence | Description |
|:--------:|:------------|
| `.` | Matches any character **except** a newline |
| `\w` | Matches any **word character** (letters, digits, underscore) |
| `\W` | Matches any **non-word character** |
| `\d` | Matches any **digit** (0-9) |
| `\D` | Matches any **non-digit** character |
| `\s` | Matches any **whitespace** character (space, tab, newline) |
| `\S` | Matches any **non-whitespace** character |

## Range Matches
Range matches use `[]` to define custom character sets. Examples:

| Pattern | Description |
|:-------:|:------------|
| `[aeiou]` | Matches any single vowel (lowercase) |
| `[a-z]` | Matches any lowercase letter |
| `[A-Z]` | Matches any uppercase letter |
| `[0-9]` | Matches any digit (same as `\d`) |
| `[a-zA-Z]` | Matches any letter (either case) |
| `[^aeiou]` | Matches any character **except** vowels |
| `[abc123]` | Matches `a`, `b`, `c`, `1`, `2`, or `3` |
