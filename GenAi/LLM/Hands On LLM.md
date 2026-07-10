Encoder -> Representing language 
- Converts input data (like text, image, audio) into a **fixed-length representation**
- **Works like**: Feature extractor 
- Example : BERT
- Input : Sequence or data 
- Output: Encoded vector representation

Decoder -> Generative Models
- **Purpose**: Takes the encoded representation and generates **output sequence** (e.g., translated text).
- **Works like**: Generator.
- Example: GPT
- **Input**: Encoded vector and previous outputs (autoregressively).
- **Output**: Sequence (e.g., a sentence in French).

Encoder - Decoder Models
- Seq2Seq (RNN Based)
- Transformer

![[Pasted image 20250718172353.png]]
![[Pasted image 20250718172423.png]]

Chain-of-Thought: Think Before Answering
![[Pasted image 20250718172528.png]]

![[Pasted image 20250718172714.png]]