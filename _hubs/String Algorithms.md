---
description: "Hub: every note about String Algorithms"
type: hub
domain: cs
tags:
  - type/hub
  - topic/string-algorithms
---
# String Algorithms

> [!info] Sparse: palindrome checks, anagrams, subsequence checks and seven small solved problems. No KMP, Z-algorithm, tries or string hashing.
> Part of [[MOC - CS Fundamentals]]. Also try the tag `#topic/string-algorithms`.

## Concepts
- [[Strings]] `stub` — Two snippets: reading a whole line with getline, and checking whether a character is a digit.

## References & cheat sheets
- [[C++ Solving Tips - Ternary And Palindrome]] — Small contest habits: rewriting an if/else as a ternary, and the two-pointer palindrome check.

## Solved problems
- [[Strings - Anagram Check]] — One-line idea plus C++ code: two words are anagrams when their sorted characters match.
- [[Strings - Night At The Museum]] — C++ solution for the circular alphabet dial with an Arabic explanation: to reach each letter, turn whichever way is shorter around the ring of 26.
- [[Strings - Decoding]] `raw` — C++ decoding solution; the comment notes this version saves more memory than the author's second attempt.
- [[Strings - Longest Palindromic Substring]] `raw` — C++ expand-around-centre solution for the longest palindromic substring, pasted with no explanation.
- [[Strings - Max Subsequences]] `raw` — C++ solution counting the maximum subsequences that can be pulled out of the given string.
- [[Strings - So And Sa]] `raw` — C++ solution that precomputes the distinct-character count of every prefix and every suffix, then maximises prefix[i] + suffix[i+1].
- [[Strings - Subsequence String]] `raw` — C++ greedy two-pointer check that one string is a subsequence of another.
- [[Strings - URL Parsing]] `raw` — C++ string solution that splits a URL into its parts.

## Related hubs
[[C++ Language]]

## Notes to self (from the audit)
- [[Strings - Anagram Check]]: No source link in the note.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
