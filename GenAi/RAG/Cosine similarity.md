```python
# Calculate cosine similarity between the search query and existing queries
def get_similarity(target, candidates):
    candidates = np.array(candidates) #convert list of candidate vectors into a numpy array
    target = np.expand_dims(np.array(target),axis=0) 
    
    # Calculate cosine similarity
    sim = cosine_similarity(target, candidates)
    sim = np.squeeze(sim).tolist()
    sort_index = np.argsort(sim)[::-1]
    sort_score = [sim[i] for i in sort_index]
    similarity_scores = zip(sort_index,sort_score)

    # Return similarity scores
    return similarity_scores

# Get the similarity between the search query and existing queries
similarity = get_similarity(new_query_embeds, embeds[:sample])
```

target -> embedding of the query 
candidates -> embedding of the docs that assume they are similar

**`target = np.expand_dims(np.array(target), axis=0)`**:
- First, it turns the target list into a NumPy array.
- Then, `np.expand_dims(..., axis=0)` adds a new dimension to the array.
- **Why?** The `cosine_similarity` function usually expects a 2D array (shape: `[n_samples, n_features]`). Since the target is just one query, this changes its shape from `(n_features,)` to `(1, n_features)`, effectively treating it as a "batch" of one item.

- **`sim = cosine_similarity(target, candidates)`**:
    - This computes the cosine similarity between the single `target` vector and every vector in the `candidates` array.
    
    - **The Result:** It returns a matrix of shape `(1, number_of_candidates)` containing scores between -1 and 1. A score closer to **1** means the vectors are very similar.

    - _Note: This assumes `from sklearn.metrics.pairwise import cosine_similarity` has been imported._

- **`sim = np.squeeze(sim).tolist()`**:
    - `np.squeeze(sim)`: Removes the extra dimension we added earlier (changing shape from `(1, n)` back to `(n,)`).
        
    - `.tolist()`: Converts the NumPy array back into a standard Python list.

- **`sort_index = np.argsort(sim)[::-1]`**:
    
    - `np.argsort(sim)`: Returns the **indices** that would sort the array. By default, it sorts in _ascending_ order (lowest score to highest).
        
    - `[::-1]`: This slices the array in reverse. It flips the order so that the indices of the **highest** similarity scores come first (descending order).

- **`sort_score = [sim[i] for i in sort_index]`**: This creates a new list of the actual similarity scores, reordered to match the sorted indices calculated in the previous step.
    
- **`similarity_scores = zip(sort_index, sort_score)`**:
    
    - This pairs up each index with its corresponding score.
        
    - The result is an iterator of tuples, looking like: `(original_index_of_candidate, similarity_score)`.
        
- **`return similarity_scores`**: Returns the zipped iterator to the caller.