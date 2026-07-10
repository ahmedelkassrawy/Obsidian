https://codeforces.com/group/5pUldkahAU/contest/511788/problem/E
[[Problem Solving/Structs]]

```C++
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

struct point {
    int x, y;
};

// Custom comparator function for sorting by y-coordinate in descending order
bool compare(const point& p1, const point& p2) {
    return p1.y > p2.y; // Sorting in descending order based on y-coordinate
}

int main() {
    int n;
    cin >> n;

    point a[n]; // Array of points

    for (int i = 0; i < n; i++) {
        cin >> a[i].x >> a[i].y; // Input x and y coordinates
    }

    // Sort points based on y-coordinate in descending order
    sort(a, a + n, compare);

    // Output the sorted points
    for (int i = 0; i < n; i++) {
        cout << a[i].x << " " << a[i].y << endl;
    }

    return 0;
}

```