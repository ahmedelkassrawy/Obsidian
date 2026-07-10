```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download necessary NLTK dat
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")


# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Get stopwords and customize exclusions
stop_words = set(stopwords.words("english"))
excluding = {"against", "no", "not", "don", "don't", "ain", "aren", "aren't", "couldn", "couldn't","didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "has", "hasn't", "haven", "haven't","isn", "isn't", "might", "mightn't", "mustn", "mustn't", "needn", "needn't", "shouldn","shouldn't", "wasn", "wasn't", "weren", "weren't", "won", "won't", "wouldn", "wouldn't"}

stop_words -= excluding

def preprocess(text):
	# Ensure input is iterable
	
	if isinstance(text, str):
		text = [text]
	
	processed = [" ".join(
			stemmer.stem(lemmatizer.lemmatize(token)  # could add pos='v'
			)
			for token in word_tokenize(sentence.lower())
			if not token.isnumeric() and token not in stop_words
		)
		for sentence in text
	]
	
	# Return same type as input
	return processed[0] if len(processed) == 1 else processed
```

```python
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download required NLTK data (run once in Colab)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLTK tools
en_stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text_series):
    # Ensure input is a pandas Series
    if not isinstance(text_series, pd.Series):
        text_series = pd.Series(text_series)
    
    def clean_text(text):
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions (@username)
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags (#hashtag)
        text = re.sub(r'#\w+', '', text)
        # Remove special characters, numbers, and extra whitespace
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords
        tokens = [word for word in tokens if word not in en_stopwords]
        # Lemmatize
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        # Join tokens back into a string
        return ' '.join(tokens)
    
    # Apply cleaning to each row in the Series
    return text_series.apply(clean_text)
df[]
df["text"] = preprocess(df["text"])
```