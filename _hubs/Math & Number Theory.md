---
description: "Hub: every note about Math & Number Theory"
type: hub
domain: cs
tags:
  - type/hub
  - topic/math-and-number-theory
---
# Math & Number Theory

> [!info] Divisors, prime factorisation, the sieve, modular arithmetic, binary exponentiation, GCD. Strong. No combinatorics or CRT.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/math-and-number-theory`.

## Concepts
- [[Number Theory - Divisors Factorization And Sieve]] — Finding all divisors by pairing around sqrt(n), three versions of prime factorisation, and the sieve used to preprocess primes so factorising becomes fast.
- [[Number Theory - Modular Arithmetic And GCD]] — The modular arithmetic toolkit: the % operator and its identities, divisor preprocessing, binary exponentiation, GCD and extended GCD, LCM and the modular inverse.

## References & cheat sheets
- [[ECPC Reference Sheet]] — The printable one-file contest sheet: complexity budget per input size, which STL container to reach for, sorting, binary search, two pointers, prefix sums, graphs, DP and number theory - each block written as concept, code, and when to use it.

## Solved problems
- [[Number Theory - Remainder Quest]] — C++ modular-arithmetic solution with an Arabic walkthrough: read the number as a string, walk it from the last digit to the first, and keep powers of ten under the modulus as you go.
- [[Number Theory - Chef And Semi Primes]] `raw` — C++ solution that decides whether a number is a semi-prime (the product of exactly two primes) using a sieve and a map.
- [[Number Theory - Hard Compare]] `raw` — C++ solution comparing two very large powers by taking logarithms instead of computing the values.
- [[Number Theory - Last 2 Digits]] `raw` — C++ solution that finds the last two digits of a large power using modular arithmetic (mod 100).
- [[Number Theory - Multiplication Of Its Divisors]] `raw` — C++ solution that multiplies all divisors of n, walking only up to sqrt(n) and pairing each divisor with its partner.

## Related hubs
[[STL Containers]], [[Dynamic Programming]], [[Graphs BFS & DFS]]

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
