#### Prompt Templates 
Prompts being input to LLMs are often structured in different ways so that we can get different results. For Q&A, we could take a user’s question and reformat it for different Q&A styles, like conventional Q&A, a bullet list of answers, or even a summary of problems relevant to the given question.

```python
from langchain import PromptTemplate

template = """Question: {question}

Answer:"""

prompt_template = PromptTemplate(
    template = template,
    input_variables = ['question']
)

question = "Which NFL team won the Super Bowl in the 2010 season?"
```

When using these prompt template with the given `question` we will get:
`Question: Which NFL team won the Super Bowl in the 2010 season? Answer:`

```python
from langchain import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             google_api_key = "AIzaSyB9o34YFREb_JLj7nXdfNwHfu5Pw9M-Hpw")

# create prompt template > LLM chain
llm_chain = LLMChain(
    prompt=prompt,
    llm=llm
)

# ask the user question about NFL 2010
print(llm_chain.run(question))
```

#### Using or Asking Multiple Questions
```python
qs = [
    {'question': "Which NFL team won the Super Bowl in the 2010 season?"},
    {'question': "If I am 6 ft 4 inches, how tall am I in centimeters?"},
    {'question': "Who was the 12th person on the moon?"},
    {'question': "How many eyes does a blade of grass have?"}
]

res = llm_chain.generate(qs)
res
```

#### Prompt Engineering
Let’s define them more precisely.

**Instructions** tell the model what to do, how to use external information if provided, what to do with the query, and how to construct the output.

**External information** or _context(s)_ act as an additional source of knowledge for the model. These can be manually inserted into the prompt, retrieved via a vector database (retrieval augmentation), or pulled in via other means (APIs, calculations, etc.).

**User input** or _query_ is typically (but not always) a query input into the system by a human user (the _prompter_).

**Output indicator** marks the _beginning_ of the to-be-generated text. If generating Python code, we may use `import` to indicate to the model that it must begin writing Python code (as most Python scripts begin with `import`).

Each component is usually placed in the prompt in this order. Starting with instructions, external information (where applicable), prompter input, and finally, the output indicator.