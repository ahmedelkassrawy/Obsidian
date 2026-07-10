---
title: "Learn What You Thought You Couldn't"
source: "https://wondering.app/lesson/3ea9cb37-b794-4497-b79e-0d3dc30d7edb/theory"
author:
  - "[[Wondering]]"
published:
created: 2026-03-12
description: "Wondering is an AI-powered learning platform that helps you learn what you thought you couldn't. Visual, interactive, and structured courses that help you learn anything in tiny chunks."
tags:
  - "clippings"
---
## What You Will Learn

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="#FFFCF0"></rect><defs><marker id="arrowhead" markerWidth="12" markerHeight="10" markerUnits="userSpaceOnUse" refX="0" refY="5" orient="auto"><polygon points="0 0, 12 5, 0 10" fill="#3C2A28"></polygon></marker></defs><rect x="275" y="40" width="250" height="80" fill="#7BCAFF" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="80" font-family="Arial, sans-serif" font-size="32" fill="#261312" text-anchor="middle" dy="0.35em">Input Words</text> <line x1="400" y1="120" x2="400" y2="168" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><text x="480" y="145" font-family="Arial, sans-serif" font-size="26" fill="#261312" text-anchor="start">Transform</text> <rect x="50" y="180" width="220" height="100" fill="#5ABDAC" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="160" y="230" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Queries</text> <rect x="290" y="180" width="220" height="100" fill="#5ABDAC" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="230" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Keys</text> <rect x="530" y="180" width="220" height="100" fill="#5ABDAC" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="640" y="230" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Values</text> <line x1="160" y1="280" x2="380" y2="345" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><line x1="400" y1="280" x2="400" y2="338" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><rect x="250" y="350" width="300" height="90" fill="#DFB431" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="395" font-family="Arial, sans-serif" font-size="32" fill="#261312" text-anchor="middle" dy="0.35em">Attention Score</text> <line x1="400" y1="440" x2="400" y2="488" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><line x1="640" y1="280" x2="450" y2="485" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><rect x="200" y="500" width="400" height="80" fill="#879A39" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="540" font-family="Arial, sans-serif" font-size="30" fill="#FFFCF0" text-anchor="middle" dy="0.35em">Contextual Meaning</text></svg>

Self-attention allows the model to weigh the importance of different words in a sequence to understand context.

## The Context Problem

How does a machine know if 'bank' refers to a river edge or a financial building?

In traditional models, words were processed in isolation or fixed windows. This made capturing deep meaning difficult.

**Self-attention** solves this. It allows each word to 'look' at every other word in a sequence to gather context.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="#FFFCF0"></rect><defs><marker id="arrowhead" markerWidth="12" markerHeight="10" markerUnits="userSpaceOnUse" refX="0" refY="5" orient="auto"><polygon points="0 0, 12 5, 0 10" fill="#3C2A28"></polygon></marker></defs><text x="400" y="60" font-family="Arial, sans-serif" font-size="36" font-weight="bold" fill="#261312" text-anchor="middle">Context-Aware Meaning </text><g><rect x="80" y="140" width="180" height="80" fill="#7BCAFF" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="170" y="180" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">River</text> <rect x="540" y="140" width="180" height="80" fill="#DFB431" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="630" y="180" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Bank</text> <path d="M 540 180 Q 400 180 272 180" fill="none" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></path><text x="400" y="150" font-family="Arial, sans-serif" font-size="26" fill="#261312" text-anchor="middle">Nature Context</text> </g><g><rect x="80" y="380" width="180" height="80" fill="#5ABDAC" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="170" y="420" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Loan</text> <rect x="540" y="380" width="180" height="80" fill="#DFB431" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="630" y="420" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Bank</text> <path d="M 540 420 Q 400 420 272 420" fill="none" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></path><text x="400" y="350" font-family="Arial, sans-serif" font-size="26" fill="#261312" text-anchor="middle">Money Context</text> </g><rect x="100" y="510" width="600" height="60" fill="#3C2A28" rx="30"></rect><text x="400" y="540" font-family="Arial, sans-serif" font-size="28" fill="#FFFCF0" text-anchor="middle" dy="0.35em">Self-Attention gathers context</text></svg>

It transforms static tokens into context-aware representations.

## Queries, Keys, and Values

To calculate attention, each token is projected into three vectors: **Query**, **Key**, and **Value**.

Think of the **Query** as what a word is looking for. The **Key** is what the word offers to others.

When a Query matches a Key, the model knows those words are related.

The **Value** holds the actual information that gets passed along once a match is found.

The Roles of Q, K, and V

| Vector    | Analogy      | Function                        |
| --------- | ------------ | ------------------------------- |
| Query (Q) | The Searcher | What the word is looking for.   |
| Key (K)   | The Label    | What the word offers to others. |
| Value (V) | The Content  | The information to be shared.   |

## Calculating the Attention Score

The model calculates a score by taking the **dot product** of the Query and Key vectors.

A high score means the two words are highly relevant to each other.

These scores are normalized to create weights. These weights determine how much of each word's **Value** vector contributes to the final output.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="#FFFCF0"></rect><defs><marker id="arrowhead" markerWidth="12" markerHeight="10" markerUnits="userSpaceOnUse" refX="0" refY="5" orient="auto"><polygon points="0 0, 12 5, 0 10" fill="#3C2A28"></polygon></marker></defs><rect x="250" y="50" width="300" height="80" fill="#7BCAFF" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="90" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Dot Product (Q×K)</text> <line x1="400" y1="130" x2="400" y2="168" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><rect x="250" y="180" width="300" height="80" fill="#5ABDAC" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="220" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Attention Scores</text> <line x1="400" y1="260" x2="400" y2="298" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><rect x="250" y="310" width="300" height="80" fill="#DFB431" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="350" font-family="Arial, sans-serif" font-size="30" fill="#261312" text-anchor="middle" dy="0.35em">Weights</text> <line x1="400" y1="390" x2="400" y2="428" stroke="#3C2A28" stroke-width="3" marker-end="url(#arrowhead)"></line><text x="460" y="415" font-family="Arial, sans-serif" font-size="26" fill="#261312" text-anchor="start">Apply to V</text> <rect x="250" y="440" width="300" height="80" fill="#879A39" stroke="#3C2A28" stroke-width="3" rx="10"></rect><text x="400" y="480" font-family="Arial, sans-serif" font-size="30" fill="#FFFCF0" text-anchor="middle" dy="0.35em">Weighted Sum</text> <text x="400" y="560" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#261312" text-anchor="middle">Attention Mechanism</text></svg>

This is the 'brain' of the Transformer architecture.

## Putting It All Together
Tracing the Self-Attention Process

1. Projection
'Apple' generates a Query looking for 'food' or 'tech' traits.
Explanation: Each word is converted into Query, Key, and Value vectors.

2. Matching
The Query for 'Apple' finds a strong match with the Key for 'fruit'.
Explanation: The Query of one word is compared against the Keys of all words.

3. Weighting
'Fruit' gets a high weight (e.g., 0.8), while 'is' gets a low weight (0.05).
Explanation: Scores are turned into weights that sum to 100%.

4. Aggregation
The new vector for 'Apple' now contains 'fruit-like' information.
Explanation: The final representation is a weighted sum of all Value vectors.