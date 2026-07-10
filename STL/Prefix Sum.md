The problem we are looking into:
[Problem - A - Codeforces](https://codeforces.com/group/isP4JMZTix/contest/386415/problem/A)
```C++
int size, range;
cin >> size >> range;
int arr[size + 1]; 
arr[0] = 0;
```
leeh array of size + 1 34an ana m4 hbtdy b zero index ana 3ayzo mn index 1
```C++
    // Read input heights and build the prefix sum array
    for (int i = 1; i <= size; ++i) {
        int height;
        cin >> height;
        arr[i] = arr[i - 1] + height;
    }
```
bad2 mn 1 zy m2oolna wb3deen ybda2 yloop w5od balk mn akbar mn aw equal size leh 34an e7na mzwdeen wa7d 3la size wb3deen arr[i] ta5od l2blha + height lda5lto so arr[0] still equals zero.

```C++
int mn,ans = 0;
    // Iterate through the possible starting points of k consecutive planks
    for (int i = 1; i <= size - range + 1; ++i) {
        int current_sum = arr[i + range - 1] - arr[i - 1];
        if (current_sum < mn) {
            mn = current_sum;
            ans = i;
        }
    }
   cout<<ans;
```

bara7a b2a start from the for condition aslan bad2een mn wa7d zy m2olna e7na 1 indexed , i asgar mn aw equal size - range + 1 --> ana bm4y m4 5atwa 5atwa laa2 ana bm4y kza 5atwa 7asb el range kam flw range 1 asln yb2a heya size bs wl range hteer m3 -1 lgmbha enma lw zy ms2la 7 size w 3 range yb2a 7 - 3 + 1 tsawy 5 lhowa a5rna 34an mfrood hzwd 3 5tawat 3lehom yb2a wslt a5r elarray

```C++
prefix[i] *= prefix[i-1]
ans = prefix[R] / prefix[L-1];
//prefix product

//prefix max
pre[i] = max( pre[i-1],arr[i] );

//prefix min
pre[i] = min( pre[i], arr[i-1] )

```

### 2D array
```C++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, m, x, y;
    cin >> n >> m >> x >> y;

    // Step 1: Read the 2D array
    int a[n][m] = {};
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> a[i][j];
        }
    }

    // Step 2: Compute the prefix sum array
    int prefix[n][m] = {};
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            prefix[i][j] = a[i][j];
            if (i > 0) prefix[i][j] += prefix[i-1][j];
            if (j > 0) prefix[i][j] += prefix[i][j-1];
            if (i > 0 && j > 0) prefix[i][j] -= prefix[i-1][j-1];
        }
    }
}

```

```C++
for (int i = 1; i <= n; i++) 
{
        for (int j = 1; j <= n; j++) 
        {
            prefix[i][j] = arr[i - 1][j - 1] 
            + prefix[i - 1][j] 
            + prefix[i][j - 1]
            - prefix[i - 1][j - 1];
        }
}


int area = prefix[y2][x2] 
			- prefix[y1 - 1][x2] 
			- prefix[y2][x1 - 1] 
			+ prefix[y1 - 1][x1 - 1];
```