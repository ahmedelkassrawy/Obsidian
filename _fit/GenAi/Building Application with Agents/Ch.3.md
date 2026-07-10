# User Experience Design for Agentic Systems

> [!abstract] User Experience in Agent Systems
> As agent systems become an integral part of our digital environments—whether through chatbots, virtual assistants, or fully autonomous workflows—the user experience (UX) they deliver plays a pivotal role in their success. While foundation models and agent architectures enable remarkable technical capabilities, how users interact with these agents ultimately determines their effectiveness, trustworthiness, and adoption. A well‑designed agent experience not only empowers users but also builds confidence, minimizes frustration, and ensures clarity in agent capabilities and limitations.

The field of agent UX is evolving at an unprecedented pace. New interface paradigms, modality combinations, and user interaction models are emerging almost monthly. This chapter provides foundational design principles that remain relevant even as the specific technologies and capabilities continue to advance rapidly.

---

## Table of Contents

1. [Interaction Modalities](#1-interaction-modalities)
   - [Overview Table](#overview-table)
2. [Text‑Based Interfaces](#2-textbased-interfaces)
3. [Graphical Interfaces (GUI)](#3-graphical-interfaces-gui)
4. [Speech and Voice Interfaces](#4-speech-and-voice-interfaces)
5. [Video‑Based Interfaces](#5-videobased-interfaces)
6. [Combining Modalities for Seamless Experiences](#6-combining-modalities-for-seamless-experiences)
7. [The Autonomy Slider](#7-the-autonomy-slider)
8. [Synchronous vs. Asynchronous Agent Experiences](#8-synchronous-vs-asynchronous-agent-experiences)
   - [Synchronous Design Principles](#synchronous-design-principles)
   - [Asynchronous Design Principles](#asynchronous-design-principles)
   - [Proactive vs. Intrusive Behavior](#proactive-vs-intrusive-behavior)
9. [Context Retention and Continuity](#9-context-retention-and-continuity)
   - [Maintaining State Across Interactions](#maintaining-state-across-interactions)
   - [Personalization and Adaptability](#personalization-and-adaptability)
10. [Communicating Agent Capabilities](#10-communicating-agent-capabilities)
11. [Communicating Confidence and Uncertainty](#11-communicating-confidence-and-uncertainty)
12. [Asking for Guidance and Input from Users](#12-asking-for-guidance-and-input-from-users)
13. [Failing Gracefully](#13-failing-gracefully)
14. [Trust in Interaction Design](#14-trust-in-interaction-design)
15. [Conclusion](#15-conclusion)

---

## 1. Interaction Modalities

Agents can interact through a variety of modalities, each offering unique strengths, limitations, and design considerations. The choice of modality shapes how users perceive and interact with agents: text‑based interfaces excel in clarity and traceability; graphical interfaces offer visual richness and intuitive controls; voice interactions provide hands‑free convenience; and video interfaces enable dynamic, real‑time communication.

### Overview Table

| Modality | Prevalence | Example Use Cases | Ideal Situations |
|----------|------------|-------------------|------------------|
| Text | Very common | Customer service chatbots, productivity assistants | When clear, asynchronous, or searchable communication is needed |
| Graphical UI (GUI) | Common | Workflow dashboards, AI coding assistants (Cursor, Windsurf) | When visual structure, context management, or multistep workflows are important |
| Speech / Voice | Less common | Siri, Alexa, Google Home, call center automation | When hands‑free interaction or natural conversation is required |
| Video | Rare | Virtual tutors, therapy avatars, interactive learning agents | When visual demonstration, rich expression, or immersive learning is needed |

Another key UX consideration: how context is managed over time. Some generative AI applications have no memory or learning – they only have the information you present in that session, requiring copy‑paste. More modern applications automatically manage context (e.g., Cursor identifies relevant code to include in each inference). Some retain memory over time, remembering past interactions and adapting to user preferences.

> [!important]
> Communicating agent capabilities, limitations, and uncertainty is essential for setting realistic user expectations and preventing misunderstandings. Users must know what an agent can and cannot do, and when they might need to intervene.

Finally, **trust and transparency** remain foundational. Predictable agent behavior and clear explanations of actions build user confidence—especially in high‑stakes scenarios.

---

## 2. Text‑Based Interfaces

Text‑based interfaces are the most common and versatile way users interact with agents – from customer service chatbots and command‑line tools to productivity assistants. They support both synchronous and asynchronous interactions, provide a traceable record of exchanges, and are easy to integrate into existing workflows.

### The Terminal Renaissance

A major shift is happening in developer tools. Tools like **Warp**, **Claude Code**, and **Gemini CLI** reimagine the terminal with AI:

- Natural language command translation
- Intelligent autocompletion
- Context‑aware explanations

These tools transform the command line into a collaborative, AI‑augmented workspace. Developers can now describe goals in plain English and have the terminal generate, run, and debug commands.

!Figure 3-1: AI‑enabled terminal interface. A demonstration of an AI‑augmented terminal, where natural language inputs are interpreted into executable commands.

> [!tip] The New Terminal
> This trend reflects a broader rethinking: the incredible natural language understanding of modern foundation models is making ordinary text‑based interactions more powerful than ever. Terminals now act as conversational partners, democratizing access to system operations, scripting, and data workflows.

### The Discoverability Problem

A key limitation of text‑based interfaces is **discoverability**. Unlike graphical interfaces with menus and buttons, text interfaces often leave users guessing what the agent can do or how to phrase commands.

**Solutions:**
- Proactive communication of supported functions (onboarding messages, periodic reminders, dynamic suggestions).
- Example: Instead of just “How can I help you today?”, say: “I can help you cancel orders, check delivery status, or update your account details.”

### Design Principles for Text‑Based Agents

- **Clarity and conciseness** – avoid jargon, long‑winded explanations.
- **Context retention** across multiturn conversations – users shouldn’t need to repeat themselves.
- **Graceful failure** – clear error messages, escalation to human, alternative suggestions.
- **Turn‑taking management** – know when to ask follow‑up questions, when to pause.
- **Ambiguity handling** – robust intent recognition for varied phrasing.
- **Length balance** – too short risks cryptic; too long overwhelms.
- **Emotional nuance** – without vocal tone or facial expressions, rely on carefully crafted language for empathy.

> [!success] Best Fit
> Text‑based agents shine in customer support (quick answers, asynchronous chat), productivity tools (command‑line, knowledge retrieval), and any scenario where precision, traceability, and searchable history are valuable.

---

## 3. Graphical Interfaces (GUI)

Graphical interfaces combine text, buttons, icons, and visual elements to create intuitive, structured interactions. They excel at reducing cognitive load through visual cues (progress bars, color coding, alert icons).

### Current Examples

- **Workflow orchestration dashboards:** LangSmith, n8n, Arize, AutoGen – show agent actions, tool calls, conditionals, and outputs as connected visual nodes.
  !Figure 3-2: Visual orchestration of an agent workflow in n8n.io.
- **AI‑enabled IDEs:** Cursor, Windsurf, Cline, GitHub Copilot – integrate natural language into coding (explanations, refactoring, debugging).
  !Figure 3-3: AI‑enabled IDE interface.

### Generative UIs – The New Frontier

Instead of static dashboards, **generative UIs** dynamically create interface elements, data visualizations, or structured outputs based on user queries.

**Example:** Perplexity AI generates structured knowledge cards, reference lists, and data tables tailored to the question. AI coding copilots generate forms, config files, or UI components from intent.

**Benefits:** Combine natural language flexibility with visual clarity and discoverability.  
**Challenges:** Ensure usability, aesthetic coherence, and avoid overwhelming users with poorly organized information.

> [!warning] Design Challenges for Graphical Agents
> - **Screen real estate** – prioritize critical information.
> - **Responsiveness** – real‑time updates and smooth state transitions.
> - **Cross‑device adaptation** – desktop, tablet, mobile.
> - **Automation vs. user control** – balance agent autonomy with user‑driven approvals.

### The Future of Professional Interfaces

Tools like Lovable, Cursor, and GitHub Copilot have redefined the developer experience. The same thinking is needed for lawyers, accountants, insurance professionals, product managers, and knowledge workers. The future of work may not revolve around documents, spreadsheets, and slide decks, but around **interactive, agent‑driven interfaces purpose‑built for decision making, analysis, and creation**.

---

## 4. Speech and Voice Interfaces

Voice interfaces offer natural, hands‑free interaction, especially valuable while driving, cooking, operating machinery, or for users with visual impairments.

### Recent Breakthroughs

Historically, latency made voice agents feel clunky. Over the past two years:

- **Low‑latency speech recognition** and efficient language processing have dramatically reduced delays.
- **Fluid, interruption‑aware** interactions – users can correct themselves mid‑sentence (“Book me a table for—oh wait, make that tomorrow instead”).
- **Tool use integration** – voice agents now schedule appointments, change system configurations, place orders, not just return answers.

### Human Processing Speeds

Humans speak at 150–180 words/min, but read at 250–300 words/min (skimming 500+). Spoken interfaces are inherently slower for dense information—voice excels when convenience and immediacy outweigh speed constraints.

### Minimal Voice Agent Implementation (FastAPI + OpenAI Realtime)

```python
import os, json, base64, asyncio, websockets
from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE = "alloy"
PCM_SR = 16000
PORT = 5050

app = FastAPI()

@app.websocket("/voice")
async def voice_bridge(ws: WebSocket):
    await ws.accept()
    openai_ws = await websockets.connect(
        "wss://api.openai.com/v1/realtime?"
        "model=gpt-4o-realtime-preview-2024-10-01",
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        },
        max_size=None, max_queue=None
    )
    # Initialize session
    await openai_ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": f"pcm_{PCM_SR}",
            "output_audio_format": f"pcm_{PCM_SR}",
            "voice": VOICE,
            "modalities": ["audio"],
            "instructions": "You are a concise AI assistant."
        }
    }))

    last_assistant_item = None
    latest_pcm_ts = 0
    pending_marks = []

    async def from_client():
        nonlocal latest_pcm_ts
        async for msg in ws.iter_text():
            data = json.loads(msg)
            pcm = base64.b64decode(data["audio"])
            latest_pcm_ts += int(len(pcm) / (PCM_SR * 2) * 1000)
            await openai_ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": base64.b64encode(pcm).decode("ascii")
            }))

    async def to_client():
        nonlocal last_assistant_item, pending_marks
        async for raw in openai_ws:
            msg = json.loads(raw)
            if msg["type"] == "response.audio.delta":
                pcm = base64.b64decode(msg["delta"])
                await ws.send_json({"audio": base64.b64encode(pcm).decode("ascii")})
                last_assistant_item = msg.get("item_id")
            elif msg["type"] == "input_audio_buffer.speech_started" and last_assistant_item:
                await openai_ws.send(json.dumps({
                    "type": "conversation.item.truncate",
                    "item_id": last_assistant_item,
                    "content_index": 0,
                    "audio_end_ms": 0
                }))
                last_assistant_item = None
                pending_marks.clear()

    try:
        await asyncio.gather(from_client(), to_client())
    finally:
        await openai_ws.close()
        await ws.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("realtime_voice_minimal:app", host="0.0.0.0", port=PORT)
```

> [!example] Future Outlook
> Voice interfaces will see wider adoption in healthcare (hands‑free note‑taking), customer service (replacing IVR systems with fluid conversations), and industrial settings (machine control while working). They are most effective for short, action‑oriented tasks.

---

## 5. Video‑Based Interfaces

Video‑based agents combine visual, auditory, and textual elements—from avatars simulating face‑to‑face conversation to agents embedded in real‑time collaboration tools.

### Strengths
- Multiple sensory channels (facial expressions, gestures, animations) add emotional nuance.
- Rich, expressive communication—useful in education, therapy, immersive learning.

### Challenges
- High processing power and bandwidth requirements.
- **Uncanny valley** – slightly off expressions can create discomfort.
- Privacy concerns with sharing visual data.

> [!info] On the Horizon
> As rendering, animation, and bandwidth improve, video agents will appear in virtual meetings, AR overlays, and digital customer service avatars, particularly in telehealth, education, and remote collaboration.

---

## 6. Combining Modalities for Seamless Experiences

The most compelling agent experiences transcend single modalities. Users don’t think in terms of modality boundaries—they just want to achieve their goals.

**Example journey:**
1. Start with voice while driving.
2. Continue via text on phone while walking.
3. Review a graphical dashboard on laptop later.
4. Receive an emailed, text‑based summary with charts.

### Design Requirements for Modality Fluidity
- **State management & context persistence** – information must never be lost during transitions.
- **Adapt communication style** – concise spoken summaries, detailed textual outputs for later review.
- **Core UX principles** remain unchanged: solve real problems, meet users where they are, build trust.

> [!quote] Keep Grounded
> The best products use technology to amplify human capability in elegant, unobtrusive ways, not merely to showcase sophistication.

---

## 7. The Autonomy Slider

A critical UX dimension is **how much autonomy the agent exercises**. As Andrej Karpathy described, effective agentic systems should let users smoothly adjust an agent’s autonomy – from fully manual to fully autonomous. This is often called an **autonomy slider**.

!Figure 3-4: The autonomy slider enables users to adjust an agent’s level of independence: Manual, Ask, Agent.

### Three Levels in a Coding IDE

- **Manual** – developer writes all code; IDE acts as a pure editor (no AI suggestions).
- **Ask (Assisted)** – agent suggests code completions, refactors, documentation; developer reviews and accepts each.
- **Agent** – agent autonomously applies standard refactors, fixes lint errors, generates boilerplate based on conventions without individual approvals.

### Three Levels in Customer Support

- **Manual** – human agents handle all queries; AI inactive or used only for backend analytics.
- **Ask (Assisted)** – agent drafts suggested replies; human reviews, edits, approves.
- **Agent** – agent autonomously handles routine queries (password resets, order tracking, FAQs); escalates complex issues.

### Design Principles for the Autonomy Slider

1. **Expose degrees of autonomy clearly** – label modes intuitively: “Manual,” “Assist,” “Auto.”
2. **Enable seamless transitions** – a toggle or slider to switch quickly.
3. **Provide predictable behavior at each level** – well‑defined actions for each mode.
4. **Communicate risks and benefits** – what’s gained/lost by increasing autonomy.
5. **Adapt based on user trust and competence** – suggest higher autonomy after demonstrated reliability.

> [!important] The autonomy slider is a trust‑building mechanism. It avoids the one‑size‑fits‑all pitfall, respects user expertise, and lets users delegate at their own pace.

---

## 8. Synchronous vs. Asynchronous Agent Experiences

Agent interactions can be **synchronous** (real‑time, back‑and‑forth) or **asynchronous** (intermittent, like email or background tasks). Choosing the right mode depends on the task, user expectations, and context.

### Synchronous Design Principles

- **Immediacy & low latency** – avoid frustrating pauses.
- **Clarity & brevity** – concise responses to maintain flow.
- **Turn‑taking mechanics** – know when to respond, wait, or escalate.
- **Visual cues** – typing indicators, progress spinners.
- **Graceful error handling** – ask clarifying questions, don’t derail interaction.

### Asynchronous Design Principles

- **Clear status communication** – what the agent is doing, estimated completion, final summary.
- **Context retention** – remember past interactions even after long delays (see Chapter 6 on memory).
- **Manage user expectations** – timelines, progress indicators, follow‑up notifications.

### Proactive vs. Intrusive Behavior

Agents must balance **proactivity** (helpful alerts, reminders) with **non‑intrusiveness**.

**Guidelines:**
- Understand user’s current focus, urgency, preferences.
- Alerts during high‑stakes video meetings → disruptive; an email notification about a completed task → appropriate.
- Prioritize relevance – notifications must add genuine value.
- Give users control over notification frequency, channels, escalation thresholds.

> [!tip] Well‑designed agents seamlessly weave proactivity into interactions, enhancing productivity without becoming overbearing.

---

## 9. Context Retention and Continuity

Context retention is both a technical capability and a **UX fundamental** – it determines whether the agent feels like a cohesive collaborator or a disconnected tool that forces users to repeat themselves.

### Implementation Approaches Impact UX

- **Client‑side only** – fast within session, but loses continuity across devices/logins.
- **Server‑side only** – cross‑device, long‑term memory, but possible latency/privacy considerations.
- **Hybrid** – short‑term on client for responsiveness, long‑term on server for continuity; often the best UX balance.

### Maintaining State Across Interactions

State management must track what happened, what’s intended, and the next logical step – crucial for multiturn conversations, task handoffs, and resumable workflows.

**Key considerations:**
- **User identity** – logged‑in users: state tied to account; anonymous: use session identifiers (cookies/tokens).
- **Persistence** – at scale, session state should live in a database or distributed cache, not just memory, to survive restarts and support load balancing.
- **Graceful recovery** – if state is lost, ask clarifying questions rather than making incorrect assumptions.
- **Security and privacy** – handle sensitive data responsibly.

### Personalization and Adaptability

Personalization goes beyond memory: it uses past behavior to tailor responses.

**Forms of personalization:**
- **Preference retention** – notification settings, common choices.
- **Behavioral adaptation** – response style, interaction flow based on user patterns.
- **Proactive assistance** – anticipating needs and offering suggestions.

**Example:** A project management agent adapts to a user’s preferred task‑tracking style. A customer service agent adjusts verbosity based on user preference.

**Challenges:** Privacy transparency (what data is stored, how it’s used); balancing adaptive vs. over‑persistent; always allow users to reset/override.

> [!quote] The best personalization feels invisible yet impactful – the agent subtly improves without drawing attention to its adjustments.

---

## 10. Communicating Agent Capabilities

Users must understand what the agent can do and how to interact with it. In traditional apps, menus and buttons provide discoverability; in agentic systems (especially text/voice), affordances are often missing.

### Strategies to Enhance Discoverability

- **Suggested action buttons** below the input field (e.g., “Track order,” “Generate summary,” “Create meeting note”).
- **Onboarding tutorials** and first‑use walkthroughs.
- **Expandable menus / capability cards** – list functions in a structured sidebar.
- **Dynamic suggestions** – based on user input, anticipate intent (“book…” → suggest “Book meeting with [name]”).
- **Agent‑led communication** – at session start: “Hi, I can help you generate content, analyze data, or summarize documents.”
- **Graceful rejection with alternatives** – “I can’t process payments directly, but I can update your billing preferences or connect you with an agent who can.”

### Progressive Disclosure & Contextual Relevance

- Don’t overwhelm – show core capabilities first, reveal advanced features as users gain comfort.
- Display the most likely actions based on current input, history, or workflow stage.
- Use visual grouping and clear hierarchy.

> [!success] Across modalities:
> - **Text chat:** quick‑reply buttons, example prompts.
> - **Graphical dashboards:** capability menus, tooltips.
> - **Voice:** list a few high‑priority options at a time.
> - **Generative UI:** dynamically produce visible, actionable outputs.

Ultimately, communicating capabilities empowers users to harness the agent confidently. Thoughtful UX transforms invisible functions into visible affordances, turning agents from opaque black boxes into transparent, collaborative partners.

---

## 11. Communicating Confidence and Uncertainty

Agents often operate probabilistically. Communicating uncertainty effectively builds trust.

**Methods:**
- **Explicit statements** – “I’m 90% certain this is the correct answer.”
- **Visual cues** – icons, color‑coded alerts, confidence meters.
- **Behavioral adjustments** – offer suggestions instead of firm recommendations when confidence is low.

> [!warning] Avoid appearing overly confident when uncertain – users quickly lose trust. Conversely, excessive hedging in low‑stakes tasks makes agents seem hesitant.

Tailor confidence communication to the stakes: critical contexts demand non‑negotiable transparency; low‑stakes settings can be more casual.

---

## 12. Asking for Guidance and Input from Users

No agent can interpret every ambiguous or vague input perfectly. Instead of guessing, agents should **ask clarifying questions**.

**Best practices:**
- Ask focused, helpful questions: “Would you like a one‑way or round‑trip ticket, and do you have preferred travel dates?”
- Reference existing context – don’t ask for information already provided.
- Explain why clarification is needed: “I need a bit more information to proceed accurately.”
- Sequence questions logically – tackle the most critical ambiguities first; avoid interrogation‑style.

> [!tip] Asking for guidance transforms uncertainty into collaboration, making the user feel like a partner rather than a subordinate.

---

## 13. Failing Gracefully

Failure is inevitable. How an agent fails can either erode or strengthen trust.

### Core Principles of Graceful Failure

- **Acknowledge transparently** – explain what went wrong simply.
- **Apologetic and empathetic language** – “I’m sorry; something went wrong while processing your request.”
- **Provide actionable next steps** – escalation to a human, troubleshooting steps, alternative resources.
- **Preserve state** – don’t force users to restart; allow them to resume where they left off.
- **Anticipate common failure points** and have predefined fallbacks (e.g., voice agent struggling → offer text input).
- **Learn from failures** – log issues, analyze patterns, feed insights back into development.

> [!quote] Failing gracefully is about maintaining user trust and minimizing frustration even when things go wrong. By being transparent, empathetic, and action‑oriented, agents turn failures into opportunities to strengthen their relationship with users.

---

## 14. Trust in Interaction Design

> [!quote] Trust is gained in drops and lost in buckets.

This certainly applies to agentic systems. Transparency and predictability are two of the most powerful tools for building trust.

### Transparency
Users need to understand:
- What the agent can do.
- Why it made a particular decision.
- What its limitations are.

Provide visibility into reasoning without overwhelming with unnecessary details. Use visual cues, status messages, and brief explanations.

### Predictability
- **Consistent behavior**: same input under same conditions → same output.
- When variability is unavoidable (probabilistic models), signal uncertainty clearly.
- Handle edge cases predictably – ask clarifying questions, provide neutral fallback, or escalate.
- **System resilience**: recover from errors, maintain state across interruptions, prevent cascading failures.

### Reliability
- Set and meet expectations consistently. If the agent claims it can handle a task, it must deliver every time.
- Misaligned expectations (overpromising, underdelivering) damage trust more than admitting limitations upfront.

---

## 15. Conclusion

Designing exceptional user experiences for agent systems goes far beyond technical functionality. It requires understanding human interaction across different modalities, contexts, and workflows. Each modality—text, GUI, voice, video—has its own strengths and tradeoffs; success comes when the modality aligns seamlessly with the user’s task, environment, and expectations.

**Synchronous vs. asynchronous** design demands thoughtful approaches to timing, responsiveness, and clarity. Synchronous interactions need immediacy; asynchronous ones need persistence and transparency. Balancing proactivity and intrusiveness remains delicate.

**Context retention and personalization** transform agents from isolated tools into reliable digital partners that remember and adapt, reducing cognitive load and fostering collaboration.

**Core UX Patterns to Remember:**
- **Communicate capabilities clearly** – onboarding, suggestions, buttons.
- **Combine modalities thoughtfully** – match text, GUI, voice, or video to task and context.
- **Retain context thoughtfully** – relevant state without violating privacy.
- **Handle errors gracefully** – clear, polite fallbacks.
- **Build trust** – be transparent about limitations, confidence, and reasoning.

Equally important: how agents communicate uncertainty, ask clarifying questions, and fail gracefully. Clear expectations, honest confidence signals, and thoughtful recovery create trust.

> [!note] Looking Ahead
> The agent landscape will continue to shift rapidly. Designers and developers must remain agile, re‑evaluating interaction paradigms and adapting to new multimodal capabilities. The principles in this chapter—clarity, adaptability, transparency, trust—provide a blueprint for creating agent experiences that are not just functional, but intuitive, engaging, and deeply aligned with human needs.

By prioritizing UX at every stage of development, we ensure agents become not just tools, but **indispensable partners** in our increasingly intelligent digital ecosystems.

---
*Next: Chapter 4 – Tool Use, moving from ordinary chatbots to systems that can do real work for users.*