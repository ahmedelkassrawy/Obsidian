---
description: "A Dragon struct plus the compare function used to sort a vector of them - the custom-comparator pattern."
domain: cs
type: reference
status: stub
tags:
  - domain/cs
  - type/reference
  - status/stub
  - topic/c-language
aliases:
  - "Structs"
  - "comparator"
hubs:
  - "[[C++ Language]]"
---
```C++
struct Dragon
{
	int strength;
	int bonus;
}

bool compare(const Dragon &a, const Dragon &b)
{
	return a.strength < b.strength;
}

int main()
{
	vector<Dragon> dragons(n)
}
```