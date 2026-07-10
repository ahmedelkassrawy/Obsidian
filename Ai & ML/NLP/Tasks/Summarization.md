```python
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("summarization", model="facebook/bart-large-cnn")


#Summarize this text
text = """In this liveProject, you can gain an overall impression of the job of a Natural Language Processing (NLP) Specialist working on the Growth Hacking Team of a freshly launched startup that is introducing a new video game to the market. One of the key targets of a growth hacking team is to enhance the massive growth of early startups in a short time. To do so, it introduces strategies with the help of which one can acquire as many customers as possible with the lowest cost as possible. As part of your team’s growth hacking strategy, your boss wants to map the field of the video game market. She aims to find out how customers evaluate your competitors’ products, namely what they like and dislike in a video game. Knowing what makes a video game attractive to a gamer helps the marketing team articulate the message of your product more effectively.
To be able to find out what makes a video game worth buying according to gamers, you need to get deeper insights into the linguistic features of their utterances. As an NLP Specialist, your task will be to analyze customers’ reviews about video games. In order to carry out this task, you will employ different NLP methods. These methods will enable you to acquire a deeper understanding of customer feedback and opinion."""


result = pipe(text)
print(result)
```