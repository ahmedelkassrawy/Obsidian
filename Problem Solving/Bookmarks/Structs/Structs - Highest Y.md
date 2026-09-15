---
description: "C++ solution that sorts an array of point structs by y descending with a custom comparator and prints them."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/c-language
aliases:
  - "Highest Y - ICPC Mansoura - Structs"
hubs:
  - "[[C++ Language]]"
---
https://codeforces.com/group/5pUldkahAU/contest/511788/problem/E
[[Problem Solving/PS Level 1/Struct With Custom Comparator]]

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