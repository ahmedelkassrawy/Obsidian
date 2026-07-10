## **Retrieval Metrics**

### **1. Actual vs. Predicted Labels**
- **Actual labels**
    - **p** = relevant context
    - **n** = irrelevant context
- **Predicted labels**
    - **p̂** = returned context
    - **n̂** = not returned
- **Confusion matrix terms**:
    - **True Positive (p p̂)** → relevant + returned
    - **True Negative (n n̂)** → irrelevant + not returned
    - **False Positive (n p̂)** → irrelevant + returned
    - **False Negative (p n̂)** → relevant + not returned
---
### **2. Context Recall (Recall@K)**
- Measures: **How many relevant contexts were retrieved?**
- Increasing @K **always raises recall**, up to perfect recall if K = dataset size.
- RAGAS default: **@K = 5**.
---
### **3. Context Precision (Precision@K)**
- Measures: **Of all retrieved contexts, how many were relevant?**
- High precision → fewer irrelevant contexts.
- Also uses **@K** → larger K generally **reduces precision**.
---
## **Generation Metrics**
### **4. Faithfulness**
- Measures: **How factually grounded the answer is in the retrieved context.**
- Range: **0 to 1**
- Uses an LLM to identify claims → sometimes imperfect.
- Low score means the answer includes claims not supported by the context.
---
### **5. Answer Relevancy**
- Measures: **How relevant and concise the answer is relative to the question.**
- Low score if:
    - Answer is incomplete.
    - Contains fluff or irrelevant info.
- Computed by:
    - LLM generating multiple questions from the answer.
    - Comparing them with the original question via cosine similarity.
---
