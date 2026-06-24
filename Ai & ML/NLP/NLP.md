# NLP Guide for Text Preprocessing and Modeling

This guide provides a comprehensive overview of natural language processing (NLP) techniques for text preprocessing, feature extraction, and modeling, tailored for tasks like sentiment analysis or text classification (e.g., using the Sentiment140 dataset). It includes code snippets for preprocessing, model training, evaluation, and saving/loading models, with a focus on Python libraries like NLTK, spaCy, scikit-learn, and transformers. The guide is structured for use in environments like Google Colab and formatted for Obsidian Markdown.

## 1. Text Preprocessing

### Lowercase Conversion

Convert text to lowercase to ensure consistency in word representations.

```python
sentence = "Her cat's name is Luna"
sentence_lower = sentence.lower()

sentence_list = [
    'Could you pass me the TV remote?',
    'It is IMPOSSIBLE to find this hotel',
    'Want to go for dinner on Tuesday?'
]
lower = [x.lower() for x in sentence_list]
```

### Stopwords Removal

Remove common words (stopwords) that carry little meaning for NLP tasks.

```python
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

en_stopwords = stopwords.words('english')

sentence = "it was too far to go to the shop and he did not want her to walk"
sentence_no_stopwords = " ".join([word for word in sentence.split() if word not in en_stopwords])
print(sentence_no_stopwords)

# Customize stopwords list
en_stopwords.remove("did")
en_stopwords.remove("not")
en_stopwords.append("go")
```

### Tokenization

Split text into sentences or words using NLTK's tokenizers.

```python
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize, sent_tokenize

sentences = "Her cat's name is Luna. Her dog's name is Max"
sentences_split = sent_tokenize(sentences)
words = word_tokenize(sentences)
```

### Stemming

Reduce words to their root form using PorterStemmer.

```python
from nltk.stem import PorterStemmer

ps = PorterStemmer()
connect_tokens = ['connecting', 'connected', 'connectivity', 'connect', 'connects']
for token in connect_tokens:
    print(f"{token} => {ps.stem(token)}")
```

### Lemmatization

Reduce words to their base or dictionary form using WordNetLemmatizer.

```python
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
for token in connect_tokens:
    print(f"{token} : {lemmatizer.lemmatize(token)}")
```

### N-grams

Generate and analyze n-grams (unigrams, bigrams, trigrams) to capture word sequences.

```python
import pandas as pd
import matplotlib.pyplot as plt

# Unigrams
uni = pd.Series(nltk.ngrams(tokens, 1)).value_counts()
uni[:10].sort_values().plot.barh(color='blue', width=0.9, figsize=(8, 8))
plt.title("10 Most Frequent Unigrams")
plt.ylabel("Unigram")
plt.xlabel("Frequency")
plt.show()

# Bigrams and Trigrams
bigrams = pd.Series(nltk.ngrams(tokens, 2)).value_counts()
trigrams = pd.Series(nltk.ngrams(tokens, 3)).value_counts()
```

### List Comprehensions for Preprocessing

Apply preprocessing steps to a DataFrame column.

```python
# Descriptive statistics for text columns
df.describe(include='object')

# Remove stopwords
df["review_lower"] = df["review_lower"].apply(lambda x: ' '.join([word for word in x.split() if word not in en_stopwords]))

# Tokenize
df["tokenized"] = df["review_no_stop"].apply(lambda x: word_tokenize(x))

# Stemming
df["stemmed"] = df["tokenized"].apply(lambda x: [ps.stem(token) for token in x])

# Lemmatization
df["lemmatized"] = df["tokenized"].apply(lambda x: [lemmatizer.lemmatize(token) for token in x])
```

## 2. Advanced NLP Techniques

### Part-of-Speech (POS) Tagging

Assign grammatical categories to words using spaCy.

```python
import spacy
import pandas as pd

nlp = spacy.load('en_core_web_sm')
text = "Emma Woodhouse, handsome, clever, and rich, with a comfortable home and happy disposition, seemed to unite some of the best blessings of existence; and had lived nearly twenty-one years in the world with very little to distress or vex her. She was the youngest of the two daughters of a most affectionate, indulgent father, and had, in consequence of her sister’s marriage, been mistress of his house from a very early period. Her mother..."

doc = nlp(text)

# Create DataFrame with tokens and POS tags
pos_df = pd.DataFrame(columns=["token", "pos_tag"])
for token in doc:
    pos_df = pd.concat([pos_df, pd.DataFrame.from_records([{'token': token.text, 'pos_tag': token.pos_}])], ignore_index=True)

# Analyze POS tag counts
pos_df_counts = pos_df.groupby(['token', 'pos_tag']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
print(pos_df_counts.head())

# Count POS tags
pos_df_poscounts = pos_df_counts.groupby(['pos_tag'])['token'].count().sort_values(ascending=False)
print(pos_df_poscounts.head())
```

### Named Entity Recognition (NER)

Identify entities (e.g., people, places) in text using spaCy.

```python
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

# Print entities
for word in doc.ents:
    print(word.text, word.label_)

# Visualize entities
displacy.render(doc, style="ent", jupyter=True)
```

## 3. Feature Engineering

### Label Encoding

Convert categorical labels to numeric values.

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(df["target"])
df["label"] = le.transform(df["target"])
```

### TF-IDF Vectorization

Convert text to numerical features using TF-IDF.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vec = TfidfVectorizer()
X_train_vec = tfidf_vec.fit_transform(X_train)
X_test_vec = tfidf_vec.transform(X_test)
```

## 4. Sentiment Analysis with Transformers

### Pre-trained Sentiment Analysis Pipeline

Use Hugging Face's transformers for quick sentiment analysis.

```python
from transformers import pipeline

sentence_1 = "i had a great time at the movie it was really funny"
sentiment_pipeline = pipeline("sentiment-analysis")
print(sentiment_pipeline(sentence_1))
```

### Custom Transformer Model

Use a domain-specific pre-trained model for sentiment analysis.

```python
model = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
print(model(sentence_1))
```

## 5. Topic Modeling with LDA

Latent Dirichlet Allocation (LDA) for identifying topics in text.

**Note**: Requires tokenized and preprocessed text. Use with libraries like `gensim`.

```python
from gensim import corpora, models

# Example: Prepare data for LDA
texts = df["tokenized"]  # List of tokenized documents
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# Train LDA model
lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)
```

## 6. Model Prediction

Predict sentiment or classification labels for custom text.

```python
def predict_spam(model, vectorizer, text):
    """
    Predicts whether a given text is spam or not using a trained model.

    Args:
        model: Trained classification model (e.g., MultinomialNB, XGBClassifier).
        vectorizer: Fitted TF-IDF vectorizer.
        text: Input text string to predict on.

    Returns:
        Predicted class label (0 for ham, 1 for spam).
    """
    cleaned_text = preprocess_text(text)  # Use your preprocess function
    text_vec = vectorizer.transform([cleaned_text])
    prediction = model.predict(text_vec)
    return prediction[0]
```

## 7. Model Saving and Loading

Save and load trained models using `joblib`.

```python
import joblib

# Save model
filename = 'final_xgb.sav'
joblib.dump(xgb, filename)

# Load model
loaded_model = joblib.load(filename)

# Example: Evaluate loaded model
# result = loaded_model.score(X_test_vec, y_test)
# print(result)
```

## 8. Recommended NLP Workflow

A streamlined to-do list for text classification tasks (e.g., sentiment analysis with Sentiment140).

1. **Initialize Preprocessing Tools**:
    - Set up stopwords, stemmer (`PorterStemmer`), and lemmatizer (`WordNetLemmatizer`).
2. **Preprocess Text**:
    - Convert to lowercase.
    - Remove URLs, mentions, hashtags, punctuation, and numbers.
    - Tokenize text (`word_tokenize`).
    - Remove stopwords.
    - Apply lemmatization (or stemming, choose one).
3. **Encode Labels**:
    - Use `LabelEncoder` for categorical labels (e.g., `0` for negative, `1` for positive).
4. **Split Data**:
    - Use `train_test_split` (e.g., 80/20 split).
5. **Vectorize Text (Traditional Models)**:
    - Apply `TfidfVectorizer` or `CountVectorizer` to training data (`fit_transform`).
    - Transform test data (`transform`).
6. **Tokenize and Pad Text (Deep Learning)**:
    - Use `Tokenizer` and set vocabulary size.
    - Convert text to sequences.
    - Define max length and pad sequences with `pad_sequences`.
7. **Train Model(s)**:
    - Traditional: `MultinomialNB`, `LogisticRegression`, `XGBClassifier`.
    - Deep Learning: LSTM or transformers (e.g., DistilBERT).
8. **Evaluate Model**:
    - Predict on test data (`y_pred`).
    - Generate `classification_report` for precision, recall, and F1-score.

## 9. Why Tokenization Before Stopwords and Lemmatization/Stemming?

- **Tokenization**: Splits text into words (e.g., "I am running" → ["I", "am", "running"]). Required before word-level operations.
- **Stopwords Removal**: Operates on tokens to remove low-value words (e.g., "the", "is").
- **Lemmatization/Stemming**: Reduces tokens to base forms (e.g., "running" → "run"). Requires tokenized input.
- **Cleaning First**: Lowercase, remove punctuation, URLs, etc., to standardize text before tokenization.
- **Lemmatization vs. Stemming**:
    - **Lemmatization**: Preserves meaning (e.g., "better" → "good"). Preferred for semantic tasks like sentiment analysis.
    - **Stemming**: Faster but less accurate (e.g., "better" → "bet"). Use for speed-critical tasks.

## Notes

- **Colab Setup**: Install required libraries (`!pip install nltk spacy transformers gensim joblib`).
- **NLTK Data**: Download resources (`nltk.download('punkt_tab')`, `nltk.download('stopwords')`, `nltk.download('wordnet')`).
- **spaCy Model**: Install `en_core_web_sm` (`!python -m spacy download en_core_web_sm`).
- **Memory Management**: For large datasets (e.g., Sentiment140), use sampling or chunking to avoid memory issues.
- **Model Choice**: Use `TfidfVectorizer` with traditional models (e.g., XGBoost) for speed, or transformers for high accuracy.

This guide provides a complete NLP workflow for text preprocessing, feature engineering, and modeling, optimized for tasks like sentiment analysis in Python environments like Google Colab.
### **Recommended NLP To-Do List**

Here’s a corrected and streamlined to-do list for a text classification task, accommodating both traditional models (e.g., MultinomialNB) and deep learning models (e.g., LSTM):

1. **Initialize Preprocessing Tools**:
    - Set up stop words, stemmer (e.g., PorterStemmer), and lemmatizer (e.g., WordNetLemmatizer).
2. **Preprocess Text**:
    - Convert text to lowercase.
    - Tokenize text.
    - Remove stop words.
    - Apply stemming or lemmatization (choose one based on task).
3. **Encode Labels**:
    - Use LabelEncoder for categorical labels if needed (e.g., convert "spam"/"ham" to 0/1).
4. **Split Data**:
    - Perform train-test split (e.g., using train_test_split).
5. **Vectorize Text (for traditional models)**:
    - Apply TfidfVectorizer or CountVectorizer to training data (fit and transform).
    - Transform test data using the fitted vectorizer.
6. **Tokenize and Pad Text (for LSTM)**:
    - Tokenize text using Tokenizer.
    - Set vocabulary size.
    - Convert text to sequences.
    - Define max length.
    - Pad sequences using pad_sequences.
7. **Train Model(s)**:
    - For traditional models: Train models like MultinomialNB, SVM, or XGBoost.
    - For LSTM: Build and train the LSTM model.
8. **Evaluate Model**:
    - Make predictions (y_pred) on test data.
    - Generate classification report using y_test and y_pred.
