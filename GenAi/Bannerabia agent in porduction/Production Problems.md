---
tags: [genai, ai-engineering, bannerabia, production, lessons]
---

## The big idea

Building an AI product is mostly normal software work. The AI model (the LLM) sits in the middle, and everything around it is regular code that you write and control.

> [!definition] LLM
> A "large language model", like Claude or GPT. You send it text, and it sends text back. It doesn't remember anything between requests unless you send that history again.

## How one message travels through the Bannerabia agent

Here is what happens every time the social media manager (the SMM) sends a message:

1. **The user sends something.** A message, maybe a PDF or photo, plus which page of the app they're on.
2. **The server checks it first, with plain code.**
	- Is this user allowed to touch this brand or workspace?
	- Did the user say "approve" to a post that's waiting for approval?
3. **The server builds the request for the AI.** It glues these pieces together, in this order:

```text
[ Tool descriptions ] + [ System prompt ] + [ Changing details ] + [ Chat history ] + [ New message ]
```

4. **The AI and its tools work back and forth.**
	- The AI reads everything and decides to use a tool (for example, `stage_draft` to prepare a post draft).
	- The server runs that tool safely and hands the result back to the AI.
	- The AI reads the result, then either replies or uses another tool.
5. **The server finishes the job, again with plain code.**
	- Shows the reply as cards and safe quick-reply buttons.
	- Saves the chat history and how much it cost.
	- Waits for a human to approve before anything gets published.

> [!definition] Tool
> An action the AI is allowed to ask for, like "save this draft" or "look at this image". The AI only asks. Your code actually does it.

> [!definition] System prompt
> The standing instructions you give the AI at the start of every request: who it is, what it should and shouldn't do.

## What went wrong

Four problems showed up once real people used it:

- We were **wasting money** on every request.
- The AI needed **too many back-and-forth turns** to finish simple things.
- Its instructions **contradicted each other**.
- It **forgot things** the user had already told it.

The sections below go through each cause and the fix.

---

## 1. Prompt caching: put the parts that never change first

AI providers offer a discount called **prompt caching**. If the start of your request is exactly the same, character for character, as a recent request, they charge you much less for that part. Reading from the cache costs about a tenth of the normal price. Writing it fresh into the cache costs 1.25 times the normal price.

> [!definition] Prompt caching
> The provider remembers the beginning of your request. If the next request starts the same way, you pay a small fee to reuse it instead of the full price.

The catch: **if even one character changes near the beginning, everything after it misses the cache**, and you pay full price again.

> [!tip] The golden rule
> Put the content that never changes first, and the content that changes (time, current page, recent activity) last.

Before cutting anything, measure first. Use Anthropic's `count_tokens` tool to see how much of the roughly 71K-token start of the request is tool descriptions (estimated at about 45–50K tokens) and how much is system prompt text (about 21K tokens). Then you know what's actually heavy instead of trimming blindly.

> [!definition] Token
> The unit AI providers count and charge by. Roughly, a token is a piece of a word. 1,000 tokens is about 750 English words.

---

## 2. What to put in the prompt, and fixing instructions that fight each other

**Context engineering** means deciding what information goes straight into the prompt, and what the AI has to go and fetch with a tool when it needs it.

> [!definition] Inlining vs. retrieval
> **Inlining** means pasting the information directly into the prompt. **Retrieval** means letting the AI fetch it with a tool only when it needs it (this is what people call RAG).

A simple way to choose:

- **Put it in the prompt** when it's small and needed almost every time. No extra steps, no tool errors, and it stays in the cache.
- **Let the AI fetch it** only when it's huge or rarely needed.

The second half of this problem matters just as much: **AI models get confused by instructions that contradict each other.** As a project grows, people keep adding rules in different files, and over time they start to disagree. This is sometimes called "prompt rot". When three sections say different things, the AI wastes turns being careful, or picks the wrong one.

The fix:

- Delete the instruction that contradicts the others.
- Design tools that help the AI correct itself when something goes wrong ("self-healing" tools).

---

## 3. What a tool sends back is also an instruction

Many people think only the system prompt steers the AI. In reality, **every piece of text a tool returns goes straight to the AI, and the AI treats it like an instruction.**

It can even carry more weight than the system prompt, because it sits at the very end of what the AI reads, and models pay most attention to what they read last.

> [!warning] Why this matters
> If a tool returns old or wrong instructions, the AI will follow them, even if your system prompt says something else. Check every message your tools send back.

---

## 4. Don't blame the AI when the brand rules are too strict

When an AI keeps writing the same robotic captions, the first instinct is to shout at it in the prompt: *"BE CREATIVE! DO NOT REPEAT YOURSELF!"*

Experienced engineers check the inputs first. If a brand guideline says *"Always include X"* and the system prompt says *"Vary your captions"*, the AI is stuck in a tug-of-war it can't win.

The fix comes in two steps:

1. **Clean up the guidelines.** Turn strict "always" rules into a list to pick from. For example: *"Pick one closing line from this list, and don't repeat any of the last 3."* The SMM approves the list for each brand.
2. **Show the AI what it wrote recently.** Only after removing the rigid templates, give the AI a short summary of recent captions. Put it in the part of the request that changes (the end), so it doesn't break the cache.

---

## 5. Know when not to use AI

This is the biggest difference between a demo and a real product:

> [!abstract] The rule
> Use the AI for things that are fuzzy or creative, like understanding a message or writing a caption. Use plain code and normal buttons for anything that has to be exact or safe: permissions, approvals, showing what changed, and small precise edits.

### A. Approvals must be decided by code, not by the AI

The AI should never decide on its own to publish a post or use admin tools. Approval has to go through plain, predictable code.

**What happened:** The SMM wrote *"the caption looks good, change this"*. Because the message included an approval phrase ("looks good") mixed with an edit request, the approval check fired instantly and treated it as an approval.

**What should happen:** The code needs a clear line between "approve" and "edit". When a message mixes both, it should be treated as an **edit**, not an approval.

### B. Let people edit directly instead of asking the AI

**What happened:** For one brand, the SMM wanted to remove a single line from a caption the AI suggested. That took 9 full AI turns, and the AI quietly changed other things too, without saying or showing what it changed.

**The fix:**

1. Let the SMM edit the caption directly on the post card in the chat, or strike out a line.
2. Instead of asking the AI to explain what changed, have the code compare the old and new versions and highlight the difference. That costs nothing and is always accurate.
3. The quick-reply buttons should **never be written freely by the AI**. They should come from a fixed list on the server, chosen by where the conversation is.

---

## 6. How the agent should remember things

AI models forget everything when a chat ends. Real products organize memory into separate levels:

| Memory level | What it holds |
| --- | --- |
| **Working memory** | The current conversation. It's kept to a manageable size by trimming old messages and summarizing them (already turned on with `AGENT_TOKEN_WINDOW_ENABLED`). |
| **Brand memory** | Rules for one client, like their brand guidelines. |
| **Workspace memory** | House rules for the whole agency that apply to every client. |

> [!warning] Never save memories silently
> If the AI quietly writes new permanent rules for itself based on one passing comment, a single misunderstood sentence can spoil every future answer. This is called **memory poisoning**. A human should always approve a new rule.

**What went wrong in Bannerabia:** There was no workspace-level memory, and the assistant never offered to remember feedback the SMM kept giving. So the SMM had to type *"don't name the dishes/plates"* **10 separate times, across 8 brands, on 7 different days.**

**The fix:**

- Add a **Workspace House Style** table next to each brand's guidelines.
- When the user gives a correction that should stick, show a **"Save as rule?"** button. Saving goes through the same safe path as everything else: preview, then human approval, then the server saves it.

---

## 7. The AI went blind to photos after the first message

Sending the full image to the AI on every turn of a long chat is expensive and can go over size limits. But if you drop the images from older messages and don't replace them with anything, the AI can't see them anymore when the user asks for changes.

**What went wrong in production:** On the first message, the photo was resized and sent properly. From the second message on, the chat history only showed a placeholder like `managed:<id> (photo "1.png") … already handled`.

So when the SMM said *"focus on the wings only"* or *"read the photo correctly, it's about Kenner"*, the AI couldn't see the photo. It either guessed or wasted turns calling `get_image_preview` to look again.

**The fix:** The first time the AI looks at a photo or video, save a detailed written description of it in `managed_media_alt_text`. On later messages, send that short description instead of the image. It's cheap, fast, and the AI still "knows" what's in the picture.

---

## The 10 lessons in short

1. **Look at real data before changing anything.** Read real chat logs and cost logs before you touch a single word of the prompt.
2. **The order of the request matters.** Tools and system prompt first, chat history next, changing details like time and current page last.
3. **Paste small info, fetch big info.** Don't make the AI use a tool to fetch a few kilobytes of text it needs on every turn.
4. **What tools return is an instruction too.** Check every message a tool sends back. Old instructions in there will take over.
5. **Fix the source rules before fighting them in the prompt.** If the guidelines say "always", a prompt saying "be varied" will lose.
6. **Use code, not AI, when it has to be exact.** Permissions, approvals, showing changes, fixed buttons, and deleting one line belong in code and the app's interface.
7. **Protect against harmful text sneaking in.** Wrap text from users and brands in clear markers and clean up anything that could break out of them (like the `neutralise()` function in `src/agent/systemPrompt.ts`, line 76). This protects against **prompt injection**, where someone hides instructions inside normal-looking text.
8. **Keep memory in separate levels and require approval.** Chat, brand, and workspace memory stay apart, and the AI never saves a permanent rule without a human saying yes.
9. **Save what the AI saw in photos as text.** Describe images the first time they're seen, so later messages stay cheap and accurate.
10. **Build tests from real cases before rewriting prompts.** Replaying real conversations lets you shorten prompts, switch settings, or upgrade the model without quietly breaking the safety rules.
