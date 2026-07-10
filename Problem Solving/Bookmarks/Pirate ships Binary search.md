```C++
#include <iostream>
#include <vector>
using namespace std;

bool canPlaceShips(int n, int k, int a, int mid, const vector<int>& shots) {
    vector<bool> shotPositions(n + 1, false);

    // Mark shot positions
    for (int i = 0; i < mid; ++i)
        shotPositions[shots[i]] = true;

    int totalShips = 0, emptyCells = 0;

    // Count valid segments for ships
    for (int i = 1; i <= n; ++i) {
        if (!shotPositions[i]) 
        {
            ++emptyCells;
            if (emptyCells == a) 
            {
                ++totalShips;
                emptyCells = 0; // Reset to ensure no touching
                ++i; // Skip one cell to avoid overlap
            }
        } 
        else 
        {
            emptyCells = 0; // Reset on hit cell
        }
    }

    return totalShips < k; // Return true if we cannot place k ships
}

int main() {
    int n, k, a, m;
    cin >> n >> k >> a >> m;

    vector<int> shots(m);
    for (int &shot : shots) cin >> shot;

    int l = 1, r = m, ans = -1;

    // Binary search for the first invalid state
    while (l <= r) 
    {
        int mid = (l + r) / 2;

        if (canPlaceShips(n, k, a, mid, shots)) 
        {
            ans = mid;
            r = mid - 1; // Try earlier moves
        } 
        else 
        {
            l = mid + 1; // Try later moves
        }
    }

    cout << ans << endl;
    return 0;
}

```