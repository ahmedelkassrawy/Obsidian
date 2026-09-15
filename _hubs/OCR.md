---
description: "Hub: every note about OCR"
type: hub
domain: ai-eng
tags:
  - type/hub
  - topic/ocr
---
# OCR

> [!info] OCR vs vision models with a confidence-threshold hybrid, and PaddleOCR basics. Practical and short.
> Part of [[MOC - AI Engineering]]. Also try the tag `#topic/ocr`.

## Concepts
- [[OCR vs VLM]] — When to use classic OCR and when to use a vision model: speed, cost, hallucination risk, handwriting accuracy, and a confidence-threshold hybrid that tries OCR first.

## How-tos & recipes
- [[PaddleOCR Basics]] `raw` — Pasted PaddleOCR notebook: initializing the detection and recognition models, extracting text with reading-order handling, and layout detection with cropped regions.

## References & cheat sheets
- [[PaddleOCR Result Structure]] — How to read a PaddleOCR result: the nested list of bounding-box corners paired with the recognized text and its confidence score.

## Meta
- [[Reading Input With Cin And Getline]] `empty` — Three scratch lines pairing a problem with a tool: semantic caching to Redis, handwriting to VLMs, printed text to OCR.

## Related hubs
[[Caching]]

## Notes to self (from the audit)
- [[Reading Input With Cin And Getline]]: Eight words - fold these three lines into the OCR and caching notes, then delete.
- [[PaddleOCR Basics]]: The LangChain agent section at the end uses the deprecated AgentExecutor API.

See also: [[Knowledge Gaps Audit 2026-09-15]] for what is still missing here.
