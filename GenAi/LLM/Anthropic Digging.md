```python
message = client.messages.create(
    model = model,
    max_tokens = 1000,
    messages = [
        {
            "role":"user",
            "content": "What is quantum computing? Answer in one sentence"
        }
    ]
)

message.content[0].text
```

#### Multi Turn Conversation
```python
def add_user_message(messages,text):
  user_message = {
      "role":"user",
      "content": text
  }
  messages.append(user_message)

def add_assistant_message(messages,text):
  assistant_message = {
      "role":"assistant",
      "content": text
  }
  messages.append(assistant_message)

def chat(messages):
  message = client.messages.create(
    model = model,
    max_tokens = 1000,
    messages = [
        {
            "role":"user",
            "content": messages
        }
      ]
    )
```

```python
# Start with an empty message list
messages = []

# Add the initial user question
add_user_message(messages, "Define quantum computing in one sentence")

# Get Claude's response
answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)

# Add a follow-up question
add_user_message(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = chat(messages)
```
