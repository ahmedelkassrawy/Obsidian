## What is a Bloom Filter?

A **Bloom Filter** is a probabilistic data structure used to test whether an element is a member of a set. It’s fast, memory-efficient, but allows for **false positives** (might say an element exists when it doesn’t). It never gives **false negatives** (if it says an element doesn’t exist, it definitely doesn’t).

### Why Use Bloom Filters?

- **Speed**: Much faster than querying a database or even a cache for existence checks.
- **Space Efficiency**: Uses minimal memory compared to storing the entire dataset.
- **Use Case**: Checking if a username exists in a system without hitting the database every time.

## How It Works

1. **Bit Array**: A Bloom Filter is a bit array of size `m` (e.g., 64 bits), initially all set to 0.
2. **Hash Functions**: Multiple hash functions (e.g., `Hash(element) % 64`) map an element to specific bit positions.
3. **Adding an Element**:
    - Compute the hash of the element (e.g., `Hash(paul) % 64 = 3`).
    - Set the corresponding bit in the array to 1 (e.g., bit 3 = 1).
4. **Checking an Element**:
    - Compute the same hash (e.g., `Hash(jack) % 64 = 63`).
    - Check if the bit is 1. If yes, the element _might_ exist. If no, it _definitely_ doesn’t.

### Example from Document

- **Checking if Username Exists**:
    
    - Query: `GET /username?q=paul`
    - Hash: `Hash(paul) % 64 = 3`
    - If bit 3 is 1, paul _might_ exist; if 0, paul _doesn’t_ exist.
    - Similarly, `Hash(jack) % 64 = 63` for `GET /username?q=jack`.
- **Adding a Username**:
    
    - Query: `POST /username?q=jack`
    - Hash: `Hash(jack) % 64 = 63`
    - Set bit 63 to 1.
    - For `POST /username?q=paul`, set bit 3 to 1 (`Hash(paul) % 64 = 3`).
- **Collisions**:
    
    - Multiple usernames can map to the same bit (e.g., `Hash(jack) % 64 = 63` and `Hash(Tim) % 64 = 63`).
    - This causes false positives (e.g., Tim might seem to exist if jack was added).

## Key Points for Study

- **False Positives**: Due to hash collisions (e.g., jack and Tim both map to bit 63).
- **No False Negatives**: If the bit is 0, the element is definitely not in the set.
- **Trade-off**: More hash functions or larger bit array reduces false positives but increases memory or computation.
- **Use Cases**:
    - Checking username availability.
    - Filtering out non-existent items before querying a database.
    - Caching optimization.

## Example Workflow

1. **Check Username**:
    - `GET /username?q=Ali` → `Hash(ali) % 64 = 4` → Check bit 4.
    - Bit 4 = 1? Ali _might_ exist. Bit 4 = 0? Ali _doesn’t_ exist.
2. **Add Username**:
    - `POST /username?q=Ali` → `Hash(ali) % 64 = 4` → Set bit 4 to 1.

## Tips for Implementation

- Choose a bit array size (`m`) based on expected elements and acceptable false positive rate.
- Use multiple hash functions for better accuracy (not shown in the document but standard practice).
- Example from document uses a simple `Hash(element) % 64`, but real implementations use robust hash functions.

## Common Pitfalls

- **Collisions**: As seen with `jack` and `Tim` mapping to bit 63, leading to potential false positives.
- **Single Hash Function**: Document uses one hash (`Hash % 64`). Real Bloom Filters use multiple to reduce collisions.
- **Fixed Size**: Bit array size (e.g., 64) limits capacity. Too small, and false positives increase.
