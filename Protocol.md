We sometimes use json then want to upgrade to SQL database
We dont want everytime to change the whole code to do the same checklist or jobs 

we just want to say hey storage save this post 
The idea is a checklist where we just specify what we want from the storgae to do :
1. Save post 
2. Get post by id
3. Update post 
4. delete post
5. list all posts

At this point we dont care how it will be done we just want it done, 
This is protocol , the checklist we wrote and dont care about its implementation

Here is the checklist written as a Protocol
```python
from typing import Protocol
from models import Post

class Storage(Protocol):
	def save(self,post:Post) -> None : ...
	def get(self,id:int) -> Post | None : ...
	def list(self) -> list[Post] : ...
	def delete(self,id:int ) -> None: ...
```

Each line is a promise of an ability 
The three dots mean we wont say how 

lets implement the helper that stores posts in JSON file
```python
class JsonStore:
	def __init__(self,path:Path) -> None:
		self.path = path
		
	def save(self,post:Post) -> None: ...
	def get(self,id:int) -> Post | None: ...
	def list(self) -> list[Post]: ...
	def delete(self,id:int) -> None: ...
```

`JsonStore` just _happens_ to have the four methods from the checklist. And that's enough. Python's checker looks at it and thinks: "this can save, get, list, and delete… so it counts as a Storage

turning an object into text is called serializing
turning it back to object is deserializing

Post -> Dict 
```python
object.model_dump(mode = "json")
```

dict -> json text -> file
```python
json.dump(...)
```

file -> json text -> dict
```python
json.load(...)
```

Validating the object is from the same class
```python
Class.model_validate(object)

raw = json.loads(self.path.read_text())
return [Post.model_validate(d) for d in raw]
#takes each dictionary `d` and rebuilds a real `Post` from it.
```