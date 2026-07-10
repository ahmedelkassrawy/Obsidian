- OCR
1-2 secs
deterministic
no hallucination
NO GPU

- VLM
10-15 secs
hallucinate
GPU,CPU

handwritten -> OCR 70-75% , VLM 80-85% 
use OCR first if the confidence score is above 90% no VLM -> go to VLM if below that confidence score

---
Hybrid usage
PyMuPDF if not text is gathered we go to the ocr or vlm
```python
class DocumentProcessor:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def process_document(self, pdf_path: str) -> str:
        """Executes the full pipeline: Segment, Classify, Route, and Reconstruct."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Could not find PDF at {pdf_path}")

        doc = fitz.open(pdf_path)
        full_markdown = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            full_markdown.append(f"\n## Page {page_num + 1}\n")
            
            blocks = page.get_text("blocks")
            blocks.sort(key=lambda b: (b[1], b[0])) 
            
            page_content = []
            for b in blocks:
                x0, y0, x1, y1, content, block_no, block_type = b
                
                if block_type == 0:  # Text
                    logger.info(f"Text block processing")
                    text = content.strip()

                    if text: 
                        page_content.append(text)
                elif block_type == 1:  # Image
                    logger.info(f"Image block processing")

                    #rectangle block
                    rect = fitz.Rect(x0, y0, x1, y1)    
                    mat = fitz.Matrix(300 / 72, 300 / 72) #adding more resolution for the ocr or vlm 

                    pix = page.get_pixmap(matrix=mat, clip=rect)

                    img = Image.open(io.BytesIO(pix.tobytes("png")))

                    ocr_text = self._ocr_image_with_gemini(img)
                    page_content.append(f"\n[Image View]\n{ocr_text}\n")
            
            # Fallback for scanned pages where no text or image blocks are tagged
            if not page_content:
                mat = fitz.Matrix(300 / 72, 300 / 72)
                pix = page.get_pixmap(matrix=mat)

                img = Image.open(io.BytesIO(pix.tobytes("png")))

                ocr_text = self._ocr_image_with_gemini(img)
                page_content.append(ocr_text)
                    
            full_markdown.extend(page_content)
                    
        return "\n\n".join(full_markdown)
```

Here's what we covered:

||Applications|Limitations|
|---|---|---|
|**OCR**|Good at parsing simple text|Bad at tables, handwriting, low-quality scans|
|**Regex**|Good at pattern matching|Bad at handling variations in text|
|**Agent**|Can adapt to variations in text|Dependent on OCR quality; otherwise may hallucinate|
