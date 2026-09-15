---
description: "C++ solution that decides whether a number is a semi-prime (the product of exactly two primes) using a sieve and a map."
domain: cs
type: solution
status: raw
tags:
  - domain/cs
  - type/solution
  - status/raw
  - topic/math-and-number-theory
aliases:
  - "Chef and semi-primes - Number Theory"
  - "semiprime"
hubs:
  - "[[Math & Number Theory]]"
---
[Sheet #3 | Number Theory 1 - Virtual Judge](https://vjudge.net/contest/663313#problem/R)****
```C++
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
using namespace std;
bool issemiprime(int n)
{
	map<int, int> m;
	int cnt = 0;
	for (int i = 2; i * i <= n; i++)
	{
		while (n % i == 0)
		{
			m[i]++;
			cnt++;
			n /= i;

		}
	}
	if (n > 1)
		cnt++, m[n]++;
	return (cnt == 2) && (m.size() == 2);
}
int main()
{
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);
	long long t;
	cin >> t;
	while (t--)
	{
		int n;
		cin >> n;
		bool flag = false;
		for (int i = 4; i <= n; i++)
		{
			if (issemiprime(i) && issemiprime(n - i))
			{
				flag = true;
				break;
			}
		}
		if (flag)
			cout << "YES\n";
		else
			cout << "NO\n";
	}
}
```