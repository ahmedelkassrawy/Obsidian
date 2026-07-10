PaddleOCR Basics
Initialize PaddleOCR with English language support. This loads two models:
- **_DET**: Text detection model (locates text regions)
- **_REC**: Text recognition model (reads characters)

```python
# Initialize English OCR model
ocr = PaddleOCR(lang='en')

image_path = 'receipt.jpg'
img = Image.open(image_path)
display(img)

result = ocr.predict(image_path)
```

Print the OCR results containing:
- **Recognized text** strings
- **Confidence scores** for each line
- **Bounding box coordinates** (localization information)

```python
page = result[0]

texts = page["rec_texts"] 
scores = page["rec_scores"]
boxes = page["rec_polys"]

for text,score,box in zip(texts,scores,boxes):
	#box is a np array like [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
	coords = box.astype(int).tolist() 
	print(f"{text:25} | {score:.3f} | {coords}")
```

PaddleOCR preprocesses images automatically—correcting rotation, deskewing, and removing noise.

The visualization below shows the preprocessed image with bounding boxes and recognized text.
```python
img = page['doc_preprocessor_res']['output_img']
```

```python
import numpy as np
import cv2
import matplotlib.pyplot as plt

img_plot = img.copy()

for text, box in zip(texts, boxes):
    # Fix: Force 32-bit integers for OpenCV
    pts = np.array(box, dtype=np.int32) 
    
    # Reshape is sometimes required by newer OpenCV versions
    pts = pts.reshape((-1, 1, 2)) 
    
    cv2.polylines(img_plot, [pts], True, (0, 255, 0), 2)
    
    # Grab the top-left coordinate for the text
    x, y = pts[0][0] 
    
    cv2.putText(img_plot, text, (x, y - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

plt.figure(figsize=(8, 10))
plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("Aligned Bounding Boxes (Processed Image)")
plt.show()
```

Create PaddleOCR Tool
```python
from langchain.tools import tool

@tool
def paddle_ocr_read_document(image_path: str) -> List[Dict[str, Any]]:
	try:
		result = ocr.predict(image_path)
		page = result[0]
		
		texts = page["rec_texts"]
		boxes = pages["rec_polys"]
		scores = pages["rec_scores"]
		
		extracted_items = []
		
		for text,box,score in zip(texts,boxes,score):
			x_coords = [point[0] for point in box]
			y_coords = [point[1] for point in box]
			
			bbox = [min(x_coords),min(y_coords),max(x_coords),max(y_coords)]
			
			item = {
				"text":text,
				"bbox": bbox,
			}
			
			if score is not None:
				item["confidence"] = score
				
			extracted_items.append(item)
			
		return extracted_items
	except Exception as e:
		return [{"error": f"Error reading image: {e}"}]
```
---
PaddleOCR Layout Detection
PaddleOCR includes a layout detection module that identifies document regions (footer, tables, charts, etc) before text extraction.

```python
from paddleocr import LayoutDetection

layout_engine = LayoutDetection()
```

This function processes images with the layout engine, returning:
- **label**: Region type (text, chart, table, etc.)
- **score**: Confidence score
- **bbox**: Bounding box coordinates

```python
def process_documet(image_path):
	layout_result = layout_engine.predict(image_path)
	
	regions = []
	for box in layout_result[0]["boxes"]:
		regions.append(
			{
				"label": box["label"],
				"score": box["score"],
				"bbox": box["coordinate"] #[x1,y1,x2,y2]
			}
		)
		
	regions.sorted(regions, 
				key = lambda x: x["score"],
				reverse = True)
	return regions
```

Visualize layout detection. Notice:
- Multiple **text** blocks
- **Paragraph_title** and **table** regions
- **Chart** with a complete bounding box (not just axis labels)
- Small elements: **number** and **footer**

```python
def visualize_layout(image_path, min_confidence=0.5):
    layout_result = layout_engine.predict(image_path)
    
    img = cv2.imread(image_path)
    img_plot = img.copy()
    
    # Get all unique labels
    labels = list(set(box['label'] for box in layout_result[0]['boxes']))
    
    # Generate colors dynamically from colormap
    cmap = colormaps.get_cmap('tab20') 
    color_map = {}
    for i, label in enumerate(labels):
        rgba = cmap(i % 20)
        # Convert to BGR (0-255) for OpenCV
        color_map[label] = (int(rgba[2]*255), int(rgba[1]*255), int(rgba[0]*255))
    
    for box in layout_result[0]['boxes']:
        if box['score'] < min_confidence:
            continue
            
        label = box['label']
        score = box['score']
        coords = box['coordinate']
        
        color = color_map[label]
        
        x1, y1, x2, y2 = [int(c) for c in coords]
        pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=int)
        
        cv2.polylines(img_plot, [pts], True, color, 2)
        text = f"{label} ({score:.2f})"
        cv2.putText(img_plot, text, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return img_plot
```

```python
result_image = visualize_layout("article.jpg", min_confidence=0.5)

# Display with matplotlib
plt.figure(figsize=(12, 14))
plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("Layout Detection Results")
plt.show()
```
---
#### Building Agentic Document Understanding
- Use PaddleOCR for text parsing and layout detection
- Use LayoutReader for sorting parsed text into reading order
- Build VLM tools for chart and table analysis

- Input: Bounding boxes normalized to 0-1000 range
- Output: Reading order position for each box

![[Pasted image 20260228144354.png]]

```python
from PIL import Image
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any
```

---
## 1.Text Extraction with PaddleOCR + LayoutLM Ordering
Extract text and determine reading order using PaddleOCR and LayoutLM.

PaddleOCR returns three components for each detected text region:
- **Recognized text** strings
- **Confidence scores**
- **Bounding box coordinates** (4-point polygons)
```python
from paddleocr import PaddleOCR

# Initialize PaddleOCR 
ocr = PaddleOCR(lang='en')

# Load image
image_path = "report_original.png"
display(Image.open(image_path))
```

```python
result = ocr.predict(image_path)
page = result[0]

texts = page['rec_texts']      # recognized text strings
scores = page['rec_scores']    # confidence scores
boxes = page['rec_polys']      # bounding box coordinates

print(f"Extracted {len(texts)} text regions")
print("\nFirst 10 regions:")

for text, score, box in list(zip(texts, scores, boxes))[:10]:
    coords = box.astype(int).tolist()
    print(f"{text:40} | {score:.3f} | {coords}")
```

1.1 Visualize
```python
processed_img = page['doc_preprocessor_res']['output_img']
img_plot = processed_img.copy()
show_text= False

for text, box in zip(texts, boxes):
    pts = np.array(box, dtype=int)
    
    cv2.polylines(img_plot, [pts], True, (0, 255, 0), 2)
    x, y = pts[0]
    
    if show_text:
        cv2.putText(img_plot, text, (x, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

plt.figure(figsize=(8, 10))
plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("Aligned Bounding Boxes (Processed Image)")
plt.show()
```

1.2 Structuring OCR Results
OCR output using an OCRRegion Schema
```python
@dataclass 
class OCRRegion:
	text:str
	bbox: list  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
	confidence: float
	
	@property
	def bbox_xyxy(self):
		x_coords = [point[0] for point in self.bbox]
		y_coords = [point[1] for point in self.bbox]
		
		return [min(x_coords),min(y_coords),max(x_coords),max(y_coords)]
		
ocr_regions: List[OCRRegion] = []
for text, score, box in zip(texts, scores, boxes):
    ocr_regions.append(OCRRegion(
        text=text, 
        bbox=box.astype(int).tolist(), 
        confidence=score
    ))

print(f"Stored {len(ocr_regions)} OCR regions")
```
---
#### Helper Functions
```python
from collections import defaultdict
from typing import List, Dict

import torch
from transformers import LayoutLMv3ForTokenClassification

MAX_LEN = 510
CLS_TOKEN_ID = 0
UNK_TOKEN_ID = 3
EOS_TOKEN_ID = 2


class DataCollator:
    def __call__(self, features: List[dict]) -> Dict[str, torch.Tensor]:
        bbox = []
        labels = []
        input_ids = []
        attention_mask = []

        # clip bbox and labels to max length, build input_ids and attention_mask
        for feature in features:
            _bbox = feature["source_boxes"]
            if len(_bbox) > MAX_LEN:
                _bbox = _bbox[:MAX_LEN]
            _labels = feature["target_index"]
            if len(_labels) > MAX_LEN:
                _labels = _labels[:MAX_LEN]
            _input_ids = [UNK_TOKEN_ID] * len(_bbox)
            _attention_mask = [1] * len(_bbox)
            assert len(_bbox) == len(_labels) == len(_input_ids) == len(_attention_mask)
            bbox.append(_bbox)
            labels.append(_labels)
            input_ids.append(_input_ids)
            attention_mask.append(_attention_mask)

        # add CLS and EOS tokens
        for i in range(len(bbox)):
            bbox[i] = [[0, 0, 0, 0]] + bbox[i] + [[0, 0, 0, 0]]
            labels[i] = [-100] + labels[i] + [-100]
            input_ids[i] = [CLS_TOKEN_ID] + input_ids[i] + [EOS_TOKEN_ID]
            attention_mask[i] = [1] + attention_mask[i] + [1]

        # padding to max length
        max_len = max(len(x) for x in bbox)
        for i in range(len(bbox)):
            bbox[i] = bbox[i] + [[0, 0, 0, 0]] * (max_len - len(bbox[i]))
            labels[i] = labels[i] + [-100] * (max_len - len(labels[i]))
            input_ids[i] = input_ids[i] + [EOS_TOKEN_ID] * (max_len - len(input_ids[i]))
            attention_mask[i] = attention_mask[i] + [0] * (
                max_len - len(attention_mask[i])
            )

        ret = {
            "bbox": torch.tensor(bbox),
            "attention_mask": torch.tensor(attention_mask),
            "labels": torch.tensor(labels),
            "input_ids": torch.tensor(input_ids),
        }
        # set label > MAX_LEN to -100, because original labels may be > MAX_LEN
        ret["labels"][ret["labels"] > MAX_LEN] = -100
        # set label > 0 to label-1, because original labels are 1-indexed
        ret["labels"][ret["labels"] > 0] -= 1
        return ret


def boxes2inputs(boxes: List[List[int]]) -> Dict[str, torch.Tensor]:
    bbox = [[0, 0, 0, 0]] + boxes + [[0, 0, 0, 0]]
    input_ids = [CLS_TOKEN_ID] + [UNK_TOKEN_ID] * len(boxes) + [EOS_TOKEN_ID]
    attention_mask = [1] + [1] * len(boxes) + [1]
    return {
        "bbox": torch.tensor([bbox]),
        "attention_mask": torch.tensor([attention_mask]),
        "input_ids": torch.tensor([input_ids]),
    }


def prepare_inputs(
    inputs: Dict[str, torch.Tensor], model: LayoutLMv3ForTokenClassification
) -> Dict[str, torch.Tensor]:
    ret = {}
    for k, v in inputs.items():
        v = v.to(model.device)
        if torch.is_floating_point(v):
            v = v.to(model.dtype)
        ret[k] = v
    return ret


def parse_logits(logits: torch.Tensor, length: int) -> List[int]:
    """
    parse logits to orders

    :param logits: logits from model
    :param length: input length
    :return: orders
    """
    logits = logits[1 : length + 1, :length]
    orders = logits.argsort(descending=False).tolist()
    ret = [o.pop() for o in orders]
    while True:
        order_to_idxes = defaultdict(list)
        for idx, order in enumerate(ret):
            order_to_idxes[order].append(idx)
        # filter idxes len > 1
        order_to_idxes = {k: v for k, v in order_to_idxes.items() if len(v) > 1}
        if not order_to_idxes:
            break
        # filter
        for order, idxes in order_to_idxes.items():
            # find original logits of idxes
            idxes_to_logit = {}
            for idx in idxes:
                idxes_to_logit[idx] = logits[idx, order]
            idxes_to_logit = sorted(
                idxes_to_logit.items(), key=lambda x: x[1], reverse=True
            )
            # keep the highest logit as order, set others to next candidate
            for idx, _ in idxes_to_logit[1:]:
                ret[idx] = orders[idx].pop()

    return ret


def check_duplicate(a: List[int]) -> bool:
    return len(a) != len(set(a))
```

#### 1.3 LayoutLM Reading Order
```python
from transformers import LayoutLMv3ForTokenClassification
from layoutreader.v3.helpers import prepare_inputs, boxes2inputs, parse_logits

print("Loading LayoutReader model...")
model_slug = "hantian/layoutreader"
layout_model = LayoutLMv3ForTokenClassification.from_pretrained(model_slug)
print("Model loaded successfully!")
```

1.4 Implement a reading order function called `get_reading_order`:
1. **Calculate image dimensions** - Estimate size from bounding boxes with 10% padding
2. **Normalize coordinates** - Scale boxes to 0-1000 range for LayoutLM
3. **Prepare inputs** - Convert to transformer format
4. **Run inference** - Get model predictions
5. **Parse results** - Extract reading order from output logits
```python
def get_reading_order(ocr_regions):
	#calc image dimensions from boudning boxes with padding
	max_y,max_y = 0,0
	
	for region in ocr_regions:
		x1,y1,x2,y2 = region.bbox_xyxy
		max_X = max(x1,x2)
		max_y = max(y1,y2)
		
	image_width = max_x * 1.1 # 10% padding
	image_height = max_y * 1.1
	
	#convert bboxes in LayoutReader format (normalized to 0-1000)
	boxes = []
	for region in ocr_regions:
		x1,y1,x2,y2 = regions.bbox_xyxy
		
		#normalize (0-1000)
		left = int((x1 / image_width) * 1000)
		top = int((y1 / image_height) * 1000)
		
		right = int((x2 / image_width) * 1000)
		bottom = int((y2 / image_hright) * 1000)
		
		boxes.append([left,top,right,bottom])
		
	#prepare inputes
	inputs = boxes2inputs(boxes)
	inputs = prepare_inputs(inputs,layout_model)
	
	#run
	logits = layout_model(**inputs).logits.cpu().squeeze(0)
	
	#parse model outputs to get reading order
	reading_order = parse_logits(logits,len(boxes))
	return reading_order
	
reading_order = get_reading_order(ocr_regions)

print(f"Reading order determined for {len(reading_order)} regions")
print(f"First 20 positions: {reading_order[:20]}")
```

1.5 Visualize
```python
import matplotlib.patches as patches

def visualize_reading_order(ocr_regions, image_array, reading_order, title="Reading Order"):
    fig, ax = plt.subplots(1, figsize=(10, 14))
    ax.imshow(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    
    # Create order mapping: index -> reading order position
    order_map = {i: order for i, order in enumerate(reading_order)}
    
    for i, region in enumerate(ocr_regions):
        bbox = region.bbox
        
        if bbox and len(bbox) >= 4:
            # Draw polygon
            ax.add_patch(patches.Polygon(bbox, linewidth=2, 
                                         edgecolor='blue',
                                         facecolor='none', alpha=0.7))
            # Add reading order number at center
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            
            ax.text(sum(xs)/len(xs), sum(ys)/len(ys), 
                    str(order_map.get(i, i)),
                    fontsize=13, color='red', 
                    ha='center', va='center', fontweight='bold')
    
    ax.set_title(title, fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.show()

visualize_reading_order(ocr_regions, processed_img, 
                        reading_order, "LayoutLM Reading Order")
```

1.6 Now Creating the ordered text output
Combine OCR text with reading order:
1. Pair each region with its reading positions
2. sort by posititon
3. return strucutred list with position,text,confidence,bbox

```python
def get_ordered_text(ocr_regions,reading_order):
	#create (reading_position,index,region) tuples and sort
	indexed_regions = [(reading_order[i] , i, ocr_regions[i])
					for i in range(len(ocr_regions))]
	
	#sort by reading_position
	indexed_regions.sort(key = lambda x: x[0])
	
	#Extract ordered text info
	ordered_text = []
	
	for postion,idx,region in indexed_regions:
		ordered_text.append(
			{
				"position": position,
				"text": region.text,
				"confidence": region.confidence,
				"bbox": region.bbox_xyxy
			}
		)
	
	return ordered_text
	
ordered_text = get_ordered_text(ocr_regions,reading_order)

print("Text in reading order:")
print("=" * 70)
ordered_text[:5]
```
---
## 2.Layout Detection with PaddleOCR
Beyond text extraction, identify **content types** using layout detection.

PaddleOCR's `LayoutDetection` identifies document structure. Each region includes:
- **label**: Content type (text, table, chart, figure, etc.)
- **score**: Confidence score
- **bbox**: Bounding box in XYXY format

```python
from paddleocr import LayoutDetection

# Initialize layout detection 
layout_engine = LayoutDetection()
```

2.1 Processing Document Layout
to identify the content types (text blocks,chart,titles,tables)
```python
def process_document(image_path):
	layout_result = layout_engine.predict(image_path)
	
	regions = []
	for box in layout_result[0]["boxes"]:
		regions.append(
			{
				"label": box["label"],
				"score": box["score"],
				"bbox": box["coordinate"] #[x1,y1,x2,y2]
			}
		)
		
	#sort by confidence
	regions= sorted(regions,lambda x: x["score"], reverse = True)
	return regions
	
layout_results = process_docment(image_path)

print(f"Detected {len(layout_results)} layout regions:")
for r in layout_results:
    print(f"  {r['label']:20} score: {r['score']:.3f}  bbox: {[int(x) for x in r['bbox']]}")
```

2.2 Structuring Layout Results
Create a LayoutRegion dataclass with unique ids
```python
@dataclass
class LayoutRegion:
	region_id: int
	region_type: str
	bbox: list
	confidence: float
	
#store layout regions in structured format
layout_regions : List[LayoutRegion] = []

for i , r in enumerate(layout_results):
	layout_regions.append(LayoutRegion(
		region_id: i,
		region_type: r["label"],
		bbox: [int(x) for x in r["bbox]],
		confidence: r["score]
	))
	
print(f"Stored {len(layout_regions)} layout regions)
```

2.3 Visualizing Layout Detection
Visualize layout regions with color coded showing region ID,type,confidence
```python
from matplotlib import colormaps

def visualize_layout(image_path,layout_regions,min_confidence = 0.5,
title = "Layout Dectection"):
	img = cv2.imread(image_path)
	img_plot = img.copy
	
	#get unique labels and generate colors
	labels = list(set(r.region_type for r in layout_regions))
	cmap = colormaps.get_cmap("tab20)
	
	color_map = {}
	for i , label in enumerate(labels):
		rgba = cmap(i % 20)
		color_map[label] = (int(rgba[2]*255), int(rgba[1]*255), int(rgba[0]*255))
		    
	for region in layout_regions:
		if region.confidence < min_confidence:
			continue
		
		x1,y1,x2,y2 = region.bbox            
		color = color_map[region.region_type]
		
		#draw rectangle
		pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=int)
        cv2.polylines(img_plot, [pts], True, color, 2)
        
		# Add label
        text = f"{region.region_id}: {region.region_type} ({region.confidence:.2f})"
        cv2.putText(img_plot, text, (x1, y1-8), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    plt.figure(figsize=(12, 16))
    plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title(title)
    plt.show()
    
    return img_plot

visualize_layout(image_path, layout_regions, 
                 min_confidence=0.5, title="PaddleOCR Layout Detection");
```

2.4 Cropping Regions for Agent Tools
Prepare cropped regions for VLM
- **Focused analysis** - VLM sees only relevant content
- **Reduced noise** - No surrounding text interference
- **Lower costs** - Smaller images reduce API costs
**Images are base64-encoded for vision API compatibility.**

```python
import base64
from io import BytesIO

#crop and save layout regions for the agent tools
def crop_regions(image,bbox,padding = 10):
	"""Crop a region from image with optional padding"""
	x1,y1,x2,y2 = bbox
	
	x1 =max(0,x1 - padding)
	y1 = max(0,y1 - padding)
	
	x2 = min(image.width, x2 + padding)
	y2 = min(image.height, y2 + padding)
	
	return image.crop((x1,y1,x2,y2))
	
def image_to_base64(img):
	"""Convert PIL Image to base64 string"""
	buffer = BytesIO()
	img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
```

```python
# Load image for cropping
pil_image = Image.open(image_path)

# Store cropped regions in dictionary
region_images = {}

for region in layout_regions:
    cropped = crop_region(pil_image, region.bbox)
    
    region_images[region.region_id] = {
        'image': cropped,
        'base64': image_to_base64(cropped),
        'type': region.region_type,
        'bbox': region.bbox
    }

print(f"Cropped {len(region_images)} regions")

# Also store full image
full_image_base64 = image_to_base64(pil_image)
```

Display all cropped regions available to the agent:
```python
# Show cropped regions
fig, axes = plt.subplots(5, 3, figsize=(15, 10))
axes = axes.flatten()

for i, (region_id, data) in enumerate(list(region_images.items())[:14]):
    axes[i].imshow(data['image'])
    axes[i].set_title(f"Region {region_id}: {data['type']}")
    axes[i].axis('off')

# Hide unused subplots
for j in range(i+1, len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.show()
```

---
#### VLM Prompts and helpers
Prompts define structured VLM output with three components:

1. **Role definition** (e.g., "Chart Analysis specialist")
2. **Extraction fields** (chart type, axes, data points)
3. **JSON template** for consistent formatting

example
```python
# Tool prompts
CHART_ANALYSIS_PROMPT = """You are a Chart Analysis specialist. 
Analyze this chart/figure image and extract:

1. **Chart Type**: (line, bar, scatter, pie, etc.)
2. **Title**: (if visible)
3. **Axes**: X-axis label, Y-axis label, and tick values
4. **Data Points**: Key values (peaks, troughs, endpoints)
5. **Trends**: Overall pattern description
6. **Legend**: (if present)

Return a JSON object with this structure:
```json
{{
  "chart_type": "...",
  "title": "...",
  "x_axis": {{"label": "...", "ticks": [...]}},
  "y_axis": {{"label": "...", "ticks": [...]}},
  "key_data_points": [...],
  "trends": "...",
  "legend": [...]
}}
```

```python
TABLE_ANALYSIS_PROMPT = """You are a Table Extraction specialist. 
Extract structured data from this table image.

1. **Identify Structure**: 
    - Column headers, row labels, data cells
2. **Extract All Data**: 
    - Preserve exact values and alignment
3. **Handle Special Cases**: 
    - Merged cells, empty cells (mark as null), multi-line headers

Return a JSON object with this structure:
```json
{{
  "table_title": "...",
  "column_headers": ["header1", "header2", ...],
  "rows": [
    {{"row_label": "...", "values": [val1, val2, ...]}},
    ...
  ],
  "notes": "any footnotes or source info"
}}
```

**VLM Helper Function**
Call VLM with multimodal messages containing prompt and base64-encoded image.
```python
def call_vlm_with_image(image_base64: str, prompt: str) -> str:
    """Call VLM with an image and prompt."""
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"}
            }
        ]
    )
    response = vlm.invoke([message])
    return response.content
```

### Creating the AnalyzeChart Tool
The `@tool` decorator converts functions to agent-usable tools. 
This tool validates region existence, retrieves cropped images, and calls the VLM with the chart analysis prompt.
```python
@tool
def AnalyzeChart(region_id: int) -> str:
    """Analyze a chart or figure region using VLM. """
     if region_id not in region_images:
        return f"Error: Region {region_id} not found. Available regions: {list(region_images.keys())}"
    
    region_data = region_images[region_id]
    
    if region_data['type'] not in ['chart', 'figure']:
        return f"Warning: Region {region_id} is type '{region_data['type']}', not a chart/figure. Proceeding anyway."
    
    result = call_vlm_with_image(region_data['base64'], CHART_ANALYSIS_PROMPT)
    
    return result

print("AnalyzeChart tool defined")
```

### Creating the AnalyzeTable Tool
Create the table extraction tool using the table-specific prompt for structured data with headers and rows.
```python
@tool
def AnalyzeTable(region_id: int) -> str:
	"""Extract structured data from a table region using VLM.
    Use this tool when you need to extract tabular data 
    with headers and rows."""
    
    if region_id not in region_images:
        return f"Error: Region {region_id} not found. Available regions: {list(region_images.keys())}"
    
    region_data = region_images[region_id]
    
    if region_data['type'] != 'table':
        return f"Warning: Region {region_id} is type '{region_data['type']}', not a table. Proceeding anyway."
    
    result = call_vlm_with_image(region_data['base64'], TABLE_ANALYSIS_PROMPT)
    return result

print("AnalyzeTable tool defined")
```
---
### 4.LangChain Agent
Build the agent to orchestrate all components:
1. Receive question about document
2. Read system prompt with OCR text and layout info
3. Decide whether to answer from text or use tools
4. Call appropriate tools for visual content
5. Combine information into coherent response

#### Formatting Context for the Agent
Convert data structures to readable text for the system prompt—the agent's "memory" of the document.
```python
#Prepare context for the agent
def format_ordered_text(ordered_text, max_items=50):
    """Format ordered text for the system prompt."""
    lines = []
    for item in ordered_text[:max_items]:
        lines.append(f"[{item['position']}] {item['text']}")
    
    if len(ordered_text) > max_items:
        lines.append(f"... and {len(ordered_text) - max_items} more text regions")
    
    return "\n".join(lines)

def format_layout_regions(layout_regions):
    """Format layout regions for the system prompt."""
    lines = []
    for region in layout_regions:
        lines.append(f"  - Region {region.region_id}: {region.region_type} (confidence: {region.confidence:.3f})")
    return "\n".join(lines)

# Create the formatted strings
ordered_text_str = format_ordered_text(ordered_text)
layout_regions_str = format_layout_regions(layout_regions)

print("Formatted context for agent:")
print(f"- Ordered text: {len(ordered_text_str)} chars")
print(f"- Layout regions: {len(layout_regions_str)} chars")
```

###  Creating the System Prompt
Construct the system prompt with:

- **Role definition**: Document Intelligence Agent
- **Document context**: OCR text in reading order
- **Layout information**: Region types and IDs
- **Tool descriptions**: When to use each tool
- **Instructions**: How to handle different content types
```python
# System prompt for the agent
SYSTEM_PROMPT = f"""You are a Document Intelligence Agent. 
You analyze documents by combining OCR text with visual analysis tools.

## Document Text (in reading order)
The following text was extracted using OCR and ordered using LayoutLM.

{ordered_text_str}

## Document Layout Regions
The following regions were detected in the document:

{layout_regions_str}

## Your Tools
- **AnalyzeChart(region_id)**: 
    - Use for chart/figure regions to extract data points, axes, and trends
- **AnalyzeTable(region_id)**: 
    - Use for table regions to extract structured tabular data

## Instructions
1. For TEXT regions: 
    - Use the OCR text provided above (it's already extracted)
2. For TABLE regions: 
    - Use the AnalyzeTable tool to get structured data
3. For CHART/FIGURE regions: 
    - Use the AnalyzeChart tool to extract visual data

When answering questions about the document, 
use the appropriate tools to get accurate information.
"""

print("System prompt created")
print(f"Total length: {len(SYSTEM_PROMPT)} characters")
```

### Assembling the Agent
Assemble the agent using `create_tool_calling_agent`
```python
# Initialize the agent (using LangChain 0.1.x API)
tools = [AnalyzeChart, AnalyzeTable]

# LLM for the agent 
agent_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM_PROMPT),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# 4. Create the tool-calling agent
agent = create_tool_calling_agent(agent_llm, tools, prompt)

# 5. Set up the AgentExecutor to run the tool-enabled loop
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

The LangChain agent uses different tools for each region.

|Component|Purpose|Output|
|---|---|---|
|**PaddleOCR**|Text Parsing|Text + bounding boxes|
|**LayoutReader**|Reading order prediction|Sorted sequence of regions|
|**PaddleOCR**|Layout Detection|Region types (table, chart, text)|
|**VLM**|Analysis of charts/tables|JSON (title, legend,... / headers, rows,...)|