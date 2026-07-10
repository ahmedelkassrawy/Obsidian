In the **skills** architecture, specialized capabilities are packaged as invokable “skills” that augment an [agent’s](https://docs.langchain.com/oss/python/langchain/agents) behavior.
Skills are primarily prompt-driven specializations that an agent can invoke on-demand.

>[!tip]
>This pattern is conceptually identical to [Agent Skills](https://agentskills.io/) and [llms.txt](https://llmstxt.org/) (introduced by Jeremy Howard), which uses tool calling for progressive disclosure of documentation. The skills pattern applies progressive disclosure to specialized prompts and domain knowledge rather than just documentation pages.

![[Pasted image 20260217184842.png]]

Key characteristics:
- Prompt driven : Skills are primarily defined by specialized prompts
- Progressive disclosure: Skills become available based on context or user needs
- Team Distribution: Diff teams can develop and maintain skills independently
- Lightweight composition: Skills are simpler than full sub-agents
- Reference awareness: Skills can reference scripts, templates, and other resources

When to use:
Use the skills pattern when you want a single [agent](https://docs.langchain.com/oss/python/langchain/agents) with many possible specializations, you don’t need to enforce specific constraints between skills, or different teams need to develop capabilities independently.
Common examples include coding assistants (skills for different languages or tasks), knowledge bases (skills for different domains), and creative assistants (skills for different formats).

```python
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt.

    Available skills:
    - write_sql: SQL query writing expert
    - review_legal_doc: Legal document reviewer

    Returns the skill's prompt and context.
    """
    # Load skill content from file/database
    ...

agent = create_agent(
    model="gpt-4.1",
    tools=[load_skill],
    system_prompt=(
        "You are a helpful assistant. "
        "You have access to two skills: "
        "write_sql and review_legal_doc. "
        "Use load_skill to access them."
    ),
)
```

Extending the pattern:
- Dynamic Tool Registration: Combine progressive disclosure with state management to register new tools as skills load.
	- For example, loading a “database_admin” skill could both add specialized context and register database-specific tools (backup, restore, migrate).
	- This uses the same tool-and-state mechanisms used across multi-agent patterns—tools updating state to dynamically change agent capabilities
	
- Hierarchical Skills: Skills can define other skills in a tree structure, creating nested specializations. 
	- For instance, loading a “data_science” skill might make available sub-skills like “pandas_expert”, “visualization”, and “statistical_analysis”.
	- Each sub-skill can be loaded independently as needed, allowing for fine-grained progressive disclosure of domain knowledge. 
	- This hierarchical approach helps manage large knowledge bases by organizing capabilities into logical groupings that can be discovered and loaded on-demand.
	
- **Reference awareness**: While each skill only has one prompt, this prompt can reference the location of other assets and provide information on when the agent should use those assets. 
	- When those assets become relevant, the agent will know that those files exist and read them into memory as needed to complete tasks. 
	- This also follows the progressive disclosure pattern and limits the information in the context window.
---
 **Progressive disclosure** - a context management technique where the agent loads information on-demand rather than upfront
 
![[Pasted image 20260217192158.png]]

- As skills grow in complexity, they may contain too much context to fit into a single `SKILL.md`, or context that’s relevant only in specific scenarios. 
- In these cases, skills can bundle additional files within the skill directory and reference them by name from `SKILL.md`. 
- These additional linked files are the **third level** (and beyond) of detail, which Claude can choose to navigate and discover only as needed.

In the PDF skill shown below, the `SKILL.md` refers to two additional files (`reference.md` and `forms.md`) that the skill author chooses to bundle alongside the core `SKILL.md`. By moving the form-filling instructions to a separate file (`forms.md`), the skill author is able to keep the core of the skill lean, trusting that Claude will read `forms.md` only when filling out a form.

![[Pasted image 20260217192502.png]]

Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable. Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed:
![[Pasted image 20260217192632.png]]

Agents with a filesystem and code execution tools don’t need to read the entirety of a skill into their context window when working on a particular task. 
This means that the amount of context that can be bundled into a skill is effectively unbounded.

![[Pasted image 20260217192825.png]]

1. To start, the context window has the core system prompt and the metadata for each of the installed skills, along with the user’s initial message;
2. Claude triggers the PDF skill by invoking a Bash tool to read the contents of `pdf/SKILL.md`;
3. Claude chooses to read the `forms.md` file bundled with the skill;
4. Finally, Claude proceeds with the user’s task now that it has loaded relevant instructions from the PDF skill.

 Pay special attention to the `name` and `description` of your skill. Claude will use these when deciding whether to trigger the skill in response to its current task.