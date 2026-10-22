- There are two post types, and each draws on its own sources. 
- The system must enforce the separation in code, not through prompt instructions.

Tech thread
- Using kb json and cited by id
- External technical resource cited by URL , written as a brief of that resource with a link back to it

Marketing Post
- Web search only , restricted to the allowed domains
- KB is prohibted in marketing posts

Why. Previously both types were written from the same knowledge base, so the feed said the same things twice in two registers. Marketing content has to come from what is happening now, which means searching.

Marketing Sources 
Add sources.json , it maps each SanadSquad service line to the domains the research agent may searchg for that service, 

Including at least 3 service lines , each with its own list , plus a global deny list
- The marketing research agent searches only within the allowlist for the service in question. It never reads kb.json .
- Every query and every URL retrieved is written to the research log, including queries that returned nothing. 
- A URL may appear in a post only if it was fetched during the run. No unretrieved links. 
- If a source fails, mark the slot as failed and continue the run.

Writing That does not read as ai output
- Banned characters: em dash, en dash used as a separator, curly quotes, emoji. 
- Banned vocabulary, loaded from a file so it can be edited without touching code. Start from: delve, leverage, tapestry, underscore, foster, pivotal, realm, landscape, crucial, seamless, robust, navigate, testament, ever-evolving. 
- Banned constructions: negative parallelism ("not just X, but Y", "not only ... but also"), copula avoidance ("serves as", "stands as", "boasts"), filler openers ("In today's fast-paced world", "It is important to note"). 
- Rule of three: flag sentences built on three parallel items when the pattern repeats within a piece. 
- Hedging density: count modal and qualifying words (may, might, could, generally, typically) per hundred words. You set the threshold and state it in your rubric. 
- Sentence length variance: generated text tends to be uniform, human writing varies. Log it per piece.