### Post
```python
import requests

url = "http://localhost:8000/complaints"
payload = {
	"id": complaint_id,
	"order_id": str(state["order_id"]), 
	"issue": state["messages"][-1].content
}

response = requests.post(url,
						json = payload)
						
print("API Response Status Code:", response.status_code)
print("API Response Text:", response.text)  
```
### Get
```python
url = f"http://localhost:8000/orders/{state['order_id']}"
try:
	response = requests.get(url)
	if response.status_code == 200:
		order_data = response.json()
```
