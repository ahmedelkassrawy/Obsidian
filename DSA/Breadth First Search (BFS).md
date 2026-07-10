- Breadth-first search allows you to find the shortest distance between two things.
- You can use breadth-first search to 
- Write a checkers AI that calculates the fewest moves to victory 
- Write a spell checker (fewest edits from your misspelling to a real word —for example, READED -> READER is one edit) 
- Find the doctor closest to you in your network

## Intro To Graphs
![[Pasted image 20240505223239.png]]
- Graph models a set of connection.

BFS helps answer 2 questions:
- Question type 1: Is there a path from node A to node B? 
- Question type 2: What is the shortest path from node A to node B?

```python
def search(name):
	search_queue = deque()
	search_queue += graph[name]
	searched = []
	while search_queue:
		person = search_queue.popleft()
		if not person in searched:
			if person_is_seller(person):
				print person + "is a mango seller"
				return True
			else:
				search_queue ++ graph[person]
				searched.append(person)
	return False
```

