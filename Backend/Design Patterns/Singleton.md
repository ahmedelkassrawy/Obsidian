Singleton Pattern is a design pattern that ensures 
- a class has only one instance 
- provides a global access point to that instance

### Why Use Singleton?
In many applications, you might want to ensure:
- Only **one object** manages shared resources (e.g., a database connection, config, model).
- That object is **reused**, not recreated, to avoid redundant work or memory issues.

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Usage
s1 = Singleton()
s2 = Singleton()

print(s1 is s2)  # True → same instance
```

example from "THE CUSTOMER SUPPORT AGENT - RAG MODULE":
```python
_rag_instance = None

def get_rag_instance():
    global _rag_instance
    
    if _rag_instance is None:
        _rag_instance = RAG()
    return _rag_instance
```

### Pros and Cons
Pros:
- Saves memory/resources	
- Easy global access to shared objects
- Guarantees consistent behavior

Cons:
- Can make testing harder
- Can lead to hidden dependencies
- Breaks pure OOP in some languages
### When to Use
- When you want to:
    - Load a **machine learning model** only once
    - Have a single **config loader**
    - Share a **database connection** across modules
    - Maintain a **global app state** in a web app or backend
