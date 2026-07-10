- If you are creating a tool -> specify the parameters and the output
- We can combine all the things together including Agents,Workflow,AgentWorkflows
```python
import os
import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.google_genai import GoogleGenAI
import os
from typing import Optional, List,Annotated
from datetime import datetime
from pydantic import BaseModel, Field
from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, get_response_synthesizer, Settings
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
import json
from pydantic import ValidationError
from llama_index.core.agent.workflow import AgentWorkflow

os.environ["GROQ_API_KEY"] = "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"
llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

Settings.llm = llm

class EmailResponse(BaseModel):
    response:str = Field(...,description = "The generated email response content")

class ParsedEmail(Event):
    sender: Optional[str]
    content: str
    subject: Optional[str]
    deadline: Optional[datetime]

class EmailParsingWorkflow(Workflow):
    @step
    async def parse(self,ev:StartEvent) -> ParsedEmail:
        prompt = f"""
        You are an expert email parser.Given the following email , Extract the following fields:
        1. sender: The name and email of the sender
        2. subject: The subject of the email    
        3. content: The main body of the email
        4. deadline: The deadline mentioned in the email if any, otherwise null

        Email:
        {ev.email_text}

        Return the result in a json format with the following structure:
        {
            "sender": "string or null",
            "subject": "string or null",
            "content": "string",
            "deadline": "ISO 8601 datetime string or null"
        }
        """

        result = await llm.acomplete(prompt)
        data = json.loads(result.text)
        return ParsedEmail(**data)
    
    @step
    async def end(self,ev:ParsedEmail) -> StopEvent:
        return StopEvent(result=ev)
    
parse_agent = FunctionAgent(
    name = "email_parser",
    description="Parse the email to extract relevant fields",
    workflow = EmailParsingWorkflow(),
)

class EmailResponse(BaseModel):
    response : str

respond_agent = FunctionAgent(
    name = "respond_agent",
    llm = llm,
    description = "Generate a professional email response based on the parsed email content and deadline",
    output_cls = EmailResponse,
    system_prompt = """You are an expert email assistant. Given the parsed email content and deadline, generate a professional and concise"""
)

email_agent_workflow = AgentWorkflow(
    agents = [parse_agent,respond_agent],
    root_agent=parse_agent.name,
)

# ──────────────────────────────
# Runner
# ──────────────────────────────
async def main():
    email_text = """
    From: Sarah Collins <sarah.collins@techwave.ai>
    To: Ahmed Elkassrawy <ahmed.elkassrawy@example.com>
    Subject: Project Update and Upcoming Submission Deadline
    Date: October 15, 2025, 10:42 AM

    Hi Ahmed,

    I hope you’re doing well. I wanted to check in regarding the AI Agent Research Report you’ve been preparing. 
    As discussed in our last meeting, we’re aiming to include your section on Retrieval-Augmented Generation (RAG) 
    pipelines in the final document.

    Please make sure to:

    - Submit your completed draft to the shared Google Drive folder.
    - Review the integration notes I sent last week.

    The final deadline is October 20, 2025 (EOD), so we can compile all contributions before our internal review.

    Let me know if you need any additional resources or time extensions.

    Best regards,
    Sarah Collins
    Project Manager – TechWave AI
    📞 +1 (415) 555-2083
    ✉️ sarah.collins@techwave.ai
    """

    result = await email_agent_workflow.run(user_msg=email_text)
    print("\n🏁 Final result:", result)


if __name__ == "__main__":
    asyncio.run(main())
```