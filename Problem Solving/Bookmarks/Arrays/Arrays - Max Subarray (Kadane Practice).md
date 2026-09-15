---
description: "Two small C++ attempts at the maximum-subarray-sum problem, kept as a scratch pad; the only prose is a reminder to trace it on Python Tutor."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/arrays-and-hashing
aliases:
  - "Max Subarray"
hubs:
  - "[[Arrays & Hashing]]"
---
```C++
#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int size;
        cin >> size;
        int arr[size];
        for (int i = 0; i < size; i++) 
        {
            cin >> arr[i];
        }

        for (int i = 0; i < size; i++) {
            int max_num = arr[i];
            for (int j = i; j < size; j++) {
                max_num = max(max_num, arr[j]);
                cout << max_num << " ";
            }
        }
        cout << "\n";
    }
    return 0;
}
```

try on python tutor 
```C++
#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t = 1;
    while (t--) {
        int size = 4;
        int arr[] = {1, 6, 3, 7};
        for (int i = 0; i < size; i++) 
        {
            int max_num = arr[i];
            for (int j = i; j < size; j++) 
            {
                max_num = max(max_num, arr[j]);
                cout << max_num << " ";
            }
        }
        cout << "\n";
    }
    return 0;
}
```

