#### Preparing text
- CountVectorizer 
- TfidfVectorizer

The corpus of text in this case is four strings in a Python list. CountVectorizer broke the strings into words, removed stop words and symbols, and converted all remaining words to lowercase. Those words comprise the columns in the dataset, and the numbers in the rows show how many times a given word appears in each string. The stop_words='english' parameter tells CountVectorizer to remove stop words using a built-in dictionary of more than 300 English-language stop words. If you prefer, you can provide your own list of stop words in a Python list. (Or you can leave the stop words in there; it often doesn’t matter.) And if you’re training with text written in another language, you can get lists of multilanguage stop words from other Python libraries such as the Natural Language Toolkit (NLTK) and Stop-words. Observe from the output that equal and equals count as separate words, even though they have similar meaning. Data scientists sometimes go a step further when preparing text for machine learning by stemming or lemmatizing words. If the preceding text were stemmed, all occurrences of equals would be converted to equal. Scikit lacks support for stemming and lemmatization, but you can get it from other libraries such as NLTK. CountVectorizer removes punctuation symbols, but it doesn’t remove numbers. It ignored the 7 in line 1 because it ignores single characters. But if you changed 7 to 777, the term 777 would appear in the vocabulary. One way to fix that is to 142 define a function that removes numbers and pass it to CountVectorizer via the preprocessor parameter: import re def preprocess_text(text): return re.sub(r'\d+', '', text).lower() vectorizer = CountVectorizer(stop_words='english', preprocessor=preprocess_text) word_matrix = vectorizer.fit_transform(lines) Note the call to lower to convert the text to lowercase. CountVectorizer doesn’t convert text to lowercase if you provide a preprocessing function, so the preprocessing function must convert it itself. It still removes punctuation characters, however. Another useful parameter to CountVectorizer is min_df, which ignores words that appear fewer than the specified number of times. It can be an integer specifying a minimum count (for example, ignore words that appear fewer than five times in the training text, or min_df=5), or it can be a floating point value from 0.0 to 1.0 specifying the minimum percentage of samples in which a word must appear—for example, ignore words that appear in less than 10% of the samples (min_df=0.1). It’s great for filtering out words that probably aren’t meaningful anyway, and it reduces memory consumption and training time by decreasing the size of the vocabulary. Count Vec tor izer also supports a max_df parameter for eliminating words that appear too frequently. The preceding examples use CountVectorizer, which probably leaves you wondering when (and why) you would use HashingVectorizer or TfidfVectorizer instead. HashingVectorizer is useful when dealing with large datasets. Rather than store 143 words in memory, it hashes each word and uses the hash as an index into an array of word counts. It can therefore do more with less memory and is very useful for reducing the size of vectorizers when serializing them so that you can restore them later—a topic I’ll say more about in Chapter 7. The downside to HashingVectorizer is that it doesn’t let you work backward from vectorized text to the original text. Count Vec tor izer does, and it provides an inverse_transform method for that purpose. TfidfVectorizer is frequently used to perform keyword extraction : examining a document or set of documents and extracting keywords that characterize their content. It assigns words numerical weights reflecting their importance, and it uses two factors to determine the weights: how often a word appears in individual documents, and how often it appears in the overall document set. Words that appear more frequently in individual documents but occur in fewer documents receive higher weights. I won’t go further into it here, but if you’re curious to learn more, this book’s GitHub repo contains a notebook that uses Tfidf Vec tor izer to extract keywords from the manuscript of Chapter 1.

```python
df = df[['title', 'genres', 'keywords', 'cast', 'director']]
df = df.fillna('')

df.head()
```

#### Feature Creation
```python
df['features'] = df['title'] + ' ' + df['genres'] + ' ' + df['keywords'] + ' ' + df['cast'] + ' ' + df['director']
```
This combined text represents the "profile" of each movie, which will be used to measure similarity.

**What’s Happening**: A single text string is created for each movie, combining all relevant attributes into a unified feature set for analysis.

```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(stop_words = "english",min_df = 20)
word_matrix = vectorizer.fit_transform(df["features"])
word_matrix.shape
```

Initializes a CountVectorizer with:
- stop_words = "english": Removes common English words (e.g., "the", "and") that don’t contribute much to meaning.
- min_df = 20: Ignores words that appear in fewer than 20 documents to reduce noise from rare terms.
- - **word_matrix = vectorizer.fit_transform(df["features"])**:
    - Transforms the features column into a sparse matrix where each row represents a movie, and each column represents a word (token) from the combined text.
    - The cell values are the count of how many times each word appears in that movie’s features.
- **word_matrix.shape**: Prints the dimensions of the matrix (e.g., number of movies × number of unique words), giving an idea of the dataset size and vocabulary.

**What’s Happening**: The text data is converted into a numerical format that can be processed by machine learning algorithms. This matrix captures the frequency of words across all movies, filtered to focus on meaningful terms.

```python
from sklearn.metrics.pairwise import cosine_similarity

sim = cosine_similarity(word_matrix)
```
What’s Happening: The similarity between all pairs of movies is calculated based on their word frequency profiles, enabling the system to find movies with similar content.

```python
def get_recomm(title,df,sim,count = 10):
  #get the row index of the specified title
  index = df.index[df["title"].str.lower() == title.lower()]

  #return an empty list if no entry
  if(len(index) == 0):
    return []

  #get corresponding row
  similarities = list(enumerate(sim[index[0]]))

  #sort the similarity scores in descending
  recommendations = sorted(similarities,key = lambda x: x[1] , reverse=True)

  #get top n recommendations
  top_recs = recommendations[1:count + 1]

  #generate a list of titles from index
  titles = []

  for i in range(len(top_recs)):
    title = df.iloc[top_recs[i][0]]["title"]
    titles.append(title)

  return titles
```

- **index = df.index[df["title"].str.lower() == title.lower()]**: Finds the index of the row where the title matches (case-insensitive). If no match, index is empty.
- **if(len(index) == 0): return []**: Returns an empty list if the title isn’t found in the dataset.
- **similarities = list(enumerate(sim[index[0]]))**: Creates a list of tuples (i, score) where i is the index of another movie, and score is its similarity to the input movie.
- **recommendations = sorted(similarities, key = lambda x: x[1], reverse=True)**: Sorts the list by similarity score in descending order (highest similarity first).
- **top_recs = recommendations[1:count + 1]**: Selects the top count recommendations, excluding the input movie itself (index 0).
- **titles = []**: Initializes a list to store recommended movie titles.
- **for i in range(len(top_recs)):**: Loops through the top recommendations, extracts the title from the DataFrame using the index, and appends it to titles.
- **return titles**: Returns the list of recommended titles.

**What’s Happening**: The function identifies a movie by title, looks up its similarity scores with all other movies, sorts them, and returns the top similar titles as recommendations.