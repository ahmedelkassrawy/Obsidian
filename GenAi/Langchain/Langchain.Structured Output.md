#### Chatbot
```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

chat_history = [
  SystemMessage(content = "You are a helpful AI assistant")
]
```

```python
while True:
  user_input = input("You: ")
  chat_history.append(HumanMessage(content = user_input))

  if user_input == "exit":
    break

  response = llm.invoke(chat_history)
  chat_history.append(AIMessage(content = response.content))
  print(f"AI: {response.content}")

print(chat_history)
```

#### Message Placeholder
**MessagesPlaceholder** – a **slot** where you dynamically insert previous conversation history (`chat_history`)
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_template = ChatPromptTemplate(
    [
        ("system","You are a helpful customer support agent"),
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human","{query}")
    ]
)

prompt = chat_template.invoke({"chat_history":chat_history,
                               "query":"Where is my refund"})
response = llm.invoke(prompt)
```
#### Prompt Template
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="""
Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}  
Explanation Length: {length_input}  
1. Mathematical Details:  
   - Include relevant mathematical equations if present in the paper.  
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.  
2. Analogies:  
   - Use relatable analogies to simplify complex ideas.  
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.  
Ensure the summary is clear, accurate, and aligned with the provided style and length.
""",
input_variables=['paper_input', 'style_input','length_input'],
)

prompt = template.invoke({"paper_input":"A4"})
result = llm.invoke(prompt)
```

#### Structured Output
#### Pydantic
```python
from pydantic import BaseModel,Field
from typing import Optional

class Student(BaseModel):
  name: str
  age: Optional[int] = None
  email: str
  cgpa: float = Field(gt = 0,
                      lt = 10)
  
new_student = {
    "name":"Kane",
    "age":19,
    "email":"abc@gmail.com",
    "cgpa":8.9
}

student = Student(**new_student)
print(student)

>> name='Kane' age=19 [email='abc@gmail.com](mailto:email='abc@gmail.com)' cgpa=8.9
```

```python
student_dict = dict(student)
print(student_dict)

>> {'name': 'Kane', 'age': 19, 'email': '[abc@gmail.com](mailto:abc@gmail.com)', 'cgpa': 8.9}
```

```python
student_json = student.model_dump_json()
print(student_json)

>> {"name":"Kane","age":19,"email":"[abc@gmail.com](mailto:abc@gmail.com)","cgpa":8.9}
```

#### With Structured Output
```python
class Review(BaseModel):

    key_themes: list[str] = Field(description="Write down all the key themes discussed in the review in a list")
    summary: str = Field(description="A brief summary of the review")
    sentiment: Literal["pos", "neg"] = Field(description="Return sentiment of the review either negative, positive or neutral")
    pros: Optional[list[str]] = Field(default=None, description="Write down all the pros inside a list")
    cons: Optional[list[str]] = Field(default=None, description="Write down all the cons inside a list")
    name: Optional[str] = Field(default=None, description="Write the name of the reviewer")
    

structured_model = model.with_structured_output(Review)

result = structured_model.invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful
                                 
Review by Nitish Singh
""")
```
#### Pydantic Parser
```python
from langchain_core.output_parsers import PydanticOutputParser
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field

class Person(BaseModel):
  name:str = Field(description = "Name of the person")
  age: int = Field(gt = 18,description = "Age of the person")
  city: str = Field(description = "Name of the city")

parser = PydanticOutputParser(pydantic_object = Person)

template = PromptTemplate(
    template = "Generate the name, age and city of a fictional {place} person \n {format_instruction}",
    input_variables = ["place"],
    partial_variables = {"format_instruction":parser.get_format_instructions()}
)

chain = template | llm | parser

response = chain.invoke({"place":"Sri Lanka"})

for m in response:
  print(m)
```
#### Conditional Chains
```python
class Feedback(BaseModel):
  sentiment: Literal["positive","negative"] = Field(description = "Give the sentiment of the feedback")

parser = StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object = Feedback)

prompt1 = PromptTemplate(
    template = "Classify the sentiment of the following feedbcak text into positive or negative \n {feedback} \n {format_instruction}",
    input_variables = ["feedback"],
    partial_variables = {"format_instruction":parser2.get_format_instructions()}
)

classifier_chain = prompt1 | llm | parser2
```

```python
prompt2 = PromptTemplate(
    template="Write an appropriate response to this positive feedback don't add unneccessary info just the feedback\n {feedback}",
    input_variables=['feedback']
)

prompt3 = PromptTemplate(
    template="Write an appropriate response to this negative feedback  don't add unneccessary info just the feedback \n {feedback}",
    input_variables=['feedback']
)
```

```python
print(chain.invoke({'feedback': 'This is a horrible phone'}))

chain.get_graph().print_ascii()
```
#### Parallel Chains
```python
prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text \n {text}',
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template='Generate 5 short question answers from the following text \n {text}',
    input_variables=['text']
)

prompt3 = PromptTemplate(
  template='Merge the provided notes and quiz into a single document \n notes -> {notes} and quiz -> {quiz}',
  input_variables=['notes', 'quiz']
)
```

```python
parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {
        "notes":prompt1 | llm | parser,
        "quiz": prompt2  | llm2 | parser
    }
)

merge_chain = prompt3 | llm | parser

chain = parallel_chain | merge_chain
```

#### Sequential Chain
```python
prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic} just the report dont add unnecessary information',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

parser = StrOutputParser()

chain = prompt1 | llm | parser | prompt2 | llm2 | parser

response = chain.invoke({'topic':'Machine Learning'})

print(response)
```

#### Runnables
#### RunnableSequence 
Sequence of Runnables, where the output of each is the input of the next.
```python
from langchain.schema.runnable import RunnableSequence

prompt1 = PromptTemplate(
    template='Write a joke about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

prompt2 = PromptTemplate(
    template = "Explain the following joke - {text}",
    input_variables = ["text"]
)

chain = RunnableSequence(prompt1,llm,parser,prompt2,llm,parser)
print(chain.invoke({"topic":"AI"}))
```

#### RunnablePassThrough
Runnable to passthrough inputs unchanged or with additional keys.
```python
from langchain.schema.runnable import RunnableSequence, RunnableParallel, RunnablePassthrough

prompt1 = PromptTemplate(
    template='Write a joke about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

prompt2 = PromptTemplate(
    template='Explain the following joke - {text}',
    input_variables=['text']
)

joke_gen_chain = RunnableSequence(prompt1, llm, parser)

parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(prompt2, llm, parser)
})

final_chain = RunnableSequence(joke_gen_chain, parallel_chain)

result = final_chain.invoke({'topic':'cricket'}) 
```

#### RunnableParallel
```python
prompt1 = PromptTemplate(
    template='Generate a tweet about {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a Linkedin post about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'tweet': RunnableSequence(prompt1, llm, parser),
    'linkedin': RunnableSequence(prompt2, llm2, parser)
})

result = parallel_chain.invoke({'topic':'AI'})

print(result['tweet'])
print(result['linkedin'])
```
#### RunnableLambda
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda

# Define word count function
def word_count(text):
    return len(text.split())

# Initialize components
prompt1 = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
llm = ChatOpenAI()  # Requires OPENAI_API_KEY environment variable
parser = StrOutputParser()

# Joke generation chain
joke_gen_chain = RunnableSequence(prompt1, llm, parser)

# Parallel processing chain
parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'word_count': RunnableLambda(word_count)
})

# Final chain
final_chain = RunnableSequence(joke_gen_chain, parallel_chain)

# Execute and format result
result = final_chain.invoke({'topic': 'AI'})
final_result = """{} \n word count - {}""".format(result['joke'], result['word_count'])
print(final_result)


>> Why did the AI go to therapy? It had an identity crisis!
>> word count - 10
```

final_result = """{} \n word count - {}""".format(result['joke'], result['word_count']) ->
the first {} is for result[joke] and the second {} for the word_count
#### RunnableBranch
```python
prompt1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Summarize the following text \n {text}',
    input_variables=['text']
)

parser = StrOutputParser()

report_gen_chain = prompt1 | llm | parser

branch_chain = RunnableBranch(
    (lambda x: len(x.split()) > 300, prompt2 | llm | parser),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_gen_chain, branch_chain)

print(final_chain.invoke({'topic':'Russia vs Ukraine'}))
```

#### Python Splitting
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter,Language

text = """
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade  # Grade is a float (like 8.5 or 9.2)

    def get_details(self):
        return self.name"

    def is_passing(self):
        return self.grade >= 6.0


# Example usage
student1 = Student("Aarav", 20, 8.2)
print(student1.get_details())

if student1.is_passing():
    print("The student is passing.")
else:
    print("The student is not passing.")

"""

# Initialize the splitter
splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=300,
    chunk_overlap=0,
)

# Perform the split
chunks = splitter.split_text(text)

for m in chunks:
  print(m)
```

