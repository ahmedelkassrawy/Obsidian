### The Nested Structure
The `result` is typically a `list` of `lists`. For a single-page image, you'll look at `result[0]`. Each item in that list looks like this:

`[ [[x0, y0], [x1, y1], [x2, y2], [x3, y3]], ("Text Content", Confidence Score) ]`

|**Level**|**Component**|**Description**|**Example**|
|---|---|---|---|
|**Outer**|`line[0]`|**Bounding Box**: A list of 4 points (x, y) starting from the top-left and going clockwise.|`[[10, 20], [100, 20], [100, 50], [10, 50]]`|
|**Inner (0)**|`line[1][0]`|**Recognized Text**: The string of text found inside those coordinates.|`"Total Amount"`|
|**Inner (1)**|`line[1][1]`|**Confidence**: A float between 0 and 1 showing how sure the model is.|`0.985`|

```python
import paddleocr
import paddle
import fitz
from PIL import Image

ocr = paddleocr.PaddleOCR(use_textline_orientation=True, lang='en')
img_path = r"D:\me\ocr\CanvasBaseImage-TRE36KJL.jpg"
result = ocr.predict(img_path)
```

Visualization:
```python
for res in result:
    print(f"Result type: {type(res)}")
    print(f"Result attributes: {dir(res)}")

    if hasattr(res, 'save_to_img'):
        res.save_to_img('ocr_result.jpg')
        print("Saved to ocr_result.jpg using save_to_img")
    elif hasattr(res, 'save_to_cv2'):
         res.save_to_cv2('ocr_result.jpg')
         print("Saved to ocr_result.jpg using save_to_cv2")
    else:
        print("Result content:", res)
```

Accessing Data
```python
for page in result:
	 for line in page: 
		 # line[0] = coordinates 
		 # line[1][0] = text 
		 # line[1][1] = score 
		 print(f"Text: {line[1][0]} | Confidence: {line[1][1]:.2f}")
```