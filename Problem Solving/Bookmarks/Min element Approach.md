```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

  
int main() {
    // Read inputs N and K
    int N, K;
    cin >> N >> K;
  
    // Read the list of numbers
    vector<int> numbers(N);
    for (int i = 0; i < N; i++) {
        cin >> numbers[i];
    }


    // Loop through the numbers in chunks of size K
    for (int i = 0; i < N; i += K) {
        // Find the minimum in the current chunk
        int min_val = 
        *min_element(numbers.begin() + i, numbers.begin() + min(i + K, N));
        cout << min_val << " ";
    }

    cout << endl;
    return 0;
}
```

the action starts from the second for loop where the min_val is taken from the derefrence of the of the min_element pointer 

min_element pointer puts a pointer starting at the numbers.begin() + i,
which at the first iteration the i = 0 so we have a pointer on the begin of the vector array,then the pointer takes the min val and stores at min_val after moving in range of numbers.begin() + min(i+k,N)

```C++
8 3
4 -1 2 3 5 0 2 7
```
- `numbers.begin() + 0` points to the start of the chunk (`4`), and `min(0 + 3, 8)` calculates the end as index 3, giving the chunk `[4, -1, 2]`.
- `min_element` finds `-1`, and `*min_element` dereferences it to return `-1`.

- `numbers.begin() + 3` points to the start of the chunk (`3`), and `min(3 + 3, 8)` gives index 6, so the chunk is `[3, 5, 0]`.
- `min_element` finds `0`, and `*min_element` returns `0`.


- `numbers.begin() + 6` points to the start (`2`), and `min(6 + 3, 8)` gives index 8, so the chunk is `[2, 7]`.
- `min_element` finds `2`, and `*min_element` returns `2`.