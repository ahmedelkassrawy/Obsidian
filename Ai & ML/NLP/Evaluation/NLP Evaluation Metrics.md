
This guide covers key evaluation metrics for generative NLP models: [[#Perplexity]], [[#ROUGE]], [[#BLEU]], and [[#METEOR]]. Use the sections below to study definitions, formulas, examples, and add your own notes.
## Overview Table

| Metric     | Primary Use         | Measures                              | Key Features                        |
| ---------- | ------------------- | ------------------------------------- | ----------------------------------- |
| Perplexity | Language Modeling   | Prediction uncertainty                | Lower is better, entropy-based      |
| ROUGE      | Text Summarization  | Overlap with reference (n-grams, LCS) | Variants: ROUGE-N, ROUGE-L, ROUGE-S |
| BLEU       | Machine Translation | N-gram precision with brevity penalty | Clipped precision, geometric mean   |
| METEOR     | Machine Translation | Precision, recall, word order         | Synonymy, stemming, alignment       |

> [!tip] Navigation Tip  
> Click the linked section titles (e.g., [[#Perplexity]]) to jump to specific metrics. Use Obsidian’s backlinks to return.

---
## Perplexity

### Definition

Perplexity measures how well a language model predicts a sequence of words. It quantifies the uncertainty in predicting the next word, derived from entropy. **Lower perplexity** indicates better model performance.
### Use Case

- Evaluating language models (e.g., predicting next word in a sentence).
- Example: A model with perplexity 10 is better than one with perplexity 50.

### Perplexity Notes

> [!note] Your Notes
> 
> - Add insights or questions about perplexity.
> - Example: How does perplexity relate to model overfitting?

---

## ROUGE

### Definition

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) evaluates text summarization by measuring overlap between generated text (hypothesis) and reference text. Variants include ROUGE-N, ROUGE-L, and ROUGE-S.

### Variants

1. **ROUGE-N**: Measures n-gram overlap.
    - Example: ROUGE-2 compares bigrams.
2. **ROUGE-L**: Measures longest common subsequence (LCS), not requiring consecutive words.
3. **ROUGE-S**: Uses skip-grams, allowing words to be separated.

### Example (ROUGE-2, ROUGE-L, ROUGE-S)

**Reference**: "The cat sits on the mat"  
**Hypothesis**: "The big cat sitting on the rug"

#### ROUGE-2

- Bigrams in Reference: `the cat`, `cat sits`, `sits on`, `on the`, `the mat` (Count: 5)
- Bigrams in Hypothesis: `the big`, `big cat`, `cat sitting`, `sitting on`, `on the`, `the rug` (Count: 6)
- Common Bigrams: `on the` (Count: 1)
- **Precision**: ( \frac{1}{6} \approx 0.167 )
- **Recall**: ( \frac{1}{5} = 0.2 )
- **F1-Score**: ( \frac{2 \times 0.167 \times 0.2}{0.167 + 0.2} \approx 0.18 )

#### ROUGE-L

- LCS: `the cat on the` (Length: 4)
- **Precision**: ( \frac{4}{7} \approx 0.571 ) (7 unigrams in hypothesis)
- **Recall**: ( \frac{4}{6} \approx 0.667 ) (6 unigrams in reference)

#### ROUGE-S

- Skip Bigrams in Reference: `the cat`, `the sits`, `cat sits`, `cat on`, `sits on`, `sits the`, `on the`, `on mat`, `the mat` (Count: 9)
- Skip Bigrams in Hypothesis: `the big`, `the cat`, `big cat`, `big sitting`, `cat sitting`, `cat on`, `sitting on`, `sitting the`, `on the`, `on rug`, `the rug` (Count: 11)
- Common Bigrams: `the cat`, `cat on`, `on the` (Count: 3)
- **Precision**: ( \frac{3}{11} \approx 0.273 )
- **Recall**: ( \frac{3}{9} \approx 0.333 )

### Use Case

- Evaluating summarization systems.
- Example: Comparing AI-generated summaries to human-written ones.

### ROUGE Notes

> [!note] Your Notes
> 
> - How do ROUGE variants differ in practical applications?
> - Add examples of when ROUGE-L is preferred over ROUGE-N.

---

## BLEU

### Definition

BLEU (Bilingual Evaluation Understudy) evaluates machine translation by comparing n-gram overlap between generated and reference translations, using **clipped precision** and a **brevity penalty**.

- **Clipped Precision**: ( \text{ClippedPrecision}_n = \frac{\text{CountClip}_n}{\text{Count}_n} )
- **Brevity Penalty (BP)**:  
    [  
    BP = \begin{cases}  
    1 & \text{if } h > r \  
    e^{\left(1 - \frac{r}{h}\right)} & \text{if } h \leq r  
    \end{cases}  
    ]  
    where (h) is hypothesis length, (r) is reference length, and (w_n) are weights.

### Example

**Reference**: "The cat sits on the mat"  
**Hypothesis**: "The big cat sitting on the mat"

- **Unigrams**: Precision = ( \frac{5}{7} \approx 0.714 )
- **Bigrams**: Precision = ( \frac{2}{6} \approx 0.333 )
- **Trигры**: Precision = ( \frac{1}{5} = 0.2 )
- **Brevity Penalty**: ( \min(1, e^{1 - \frac{6}{7}}) = 1 )
- **BLEU Score** (with weights ( w = {0.5, 0.25, 0.25} )):  
  

### Use Case

- Evaluating machine translation systems.
- Example: Comparing Google Translate output to human translations.

### BLEU Notes

> [!note] Your Notes
> 
> - Why is clipped precision important?
> - Explore how brevity penalty affects short translations.

---

## METEOR

### Definition

METEOR (Metric for Evaluation of Translation with Explicit ORdering) evaluates translation quality by considering precision, recall, synonymy, stemming, and word order. It uses word alignment and a penalty for incorrect ordering.


- **Harmonic Mean**: ( \frac{\text{Precision} \times \text{Recall}}{\alpha \times \text{Precision} + (1 - \alpha) \times \text{Recall}} )
- **Penalty**: ( \gamma \times \left( \frac{\text{ch}}{\text{m}} \right)^3 )  
    where (\text{ch}) is number of chunks, (\text{m}) is number of matches, (\gamma) is a parameter (e.g., 0.8), and (\alpha) is a weighting factor (e.g., 0.5).

### Example

**Reference**: "The cat sits on the mat"  
**Hypothesis**: "The big cat sitting on the rug"

- **Matches (m)**: 4 (`the`, `cat`, `on`, `the`)
- **Precision**: ( \frac{4}{7} \approx 0.571 )
- **Recall**: ( \frac{4}{6} \approx 0.667 )
- **Harmonic Mean** ((\alpha = 0.5)): ( \frac{0.571 \times 0.667}{0.5 \times 0.571 + 0.5 \times 0.667} \approx 0.61 )
- **Penalty** ((\gamma = 0.8), 3 chunks): ( 0.8 \times \left( \frac{3}{4} \right)^3 \approx 0.34 )
- **METEOR Score**: ( (1 - 0.34) \times 0.61 \approx 0.41 )

### Use Case

- Evaluating translations with focus on semantic similarity.
- Example: Comparing translations where synonyms or word order vary.

### METEOR Notes

> [!note] Your Notes
> 
> - How does METEOR’s use of synonyms improve evaluation?
> - Add examples of chunking in word alignment.

---

> [!question] Reflection Questions
> 
> - Which metric is best for evaluating chatbots? Why?
> - How do these metrics handle multilingual texts?