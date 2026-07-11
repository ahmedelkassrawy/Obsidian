##### Components of API
![[Pasted image 20260120151916.png]]
SQLAlchemy -> Object-Relational Mapping (ORM) library to connect Python to DB

This summary breaks down the `crud.py` file, which utilizes SQLAlchemy to interact with the fantasy sports database. The focus is on **Read-only** operations designed for both standard application use and AI-driven analytics.

---
## 🛠️ Core Components & Imports

The script relies on **SQLAlchemy ORM** to bridge Python classes and SQL tables:

* `Session`: Manages the database connection and transaction.
* `joinedload`: Implements **Eager Loading** to fetch related data in a single query.
* `date`: Enables filtering records by time-based criteria.
* `models`: A local reference to the SQLAlchemy classes (Player, Team, League, etc.).

---
## 🔍 Query Functions

### 1. Basic Lookups (`get_player`)

Retrieves a single record by its primary key (`player_id`). Because the primary key is unique, this function returns a single instance or null.

### 2. Paginated & Filtered Lists (`get_players`)

This function handles larger datasets using three main techniques:

* **Pagination:** Uses `.offset(skip)` and `.limit(limit)` to return data in chunks (e.g., records 20–40).
* **Dynamic Filtering:** Checks if parameters like `min_last_changed_date`, `first_name`, or `last_name` are provided, appending `.filter()` clauses only when needed.
* **Defaults:** `skip` defaults to 0 and `limit` to 100 to ensure the API doesn't crash from over-fetching.

### 3. Eager Loading (`get_leagues`)

Uses `joinedload(models.League.teams)`.

> **Concept:** Instead of making one query for a league and then separate queries for every team in that league (the "N+1 problem"), it performs a SQL **JOIN** to grab all related teams immediately.

---

## 📈 AI & Analytics Support

To support Large Language Models (LLMs) and efficient front-ends, the script includes specific **Count** functions:

* `get_player_count`
* `get_team_count`
* `get_league_count`

**Why this matters for AI:** LLMs need to know the scale of the data before requesting it. By providing a count endpoint, the AI can plan pagination or answer questions like "How many leagues are there?" without downloading thousands of rows of data.

---
## 🏗️ Architectural Summary

| Feature | Implementation | Purpose |
| --- | --- | --- |
| **Read Logic** | `db.query().filter()` | Implements the "R" in CRUD. |
| **Performance** | `joinedload` | Reduces database round-trips. |
| **UX/UI Support** | `skip` & `limit` | Enables smooth scrolling and page navigation. |
| **AI Optimization** | `.count()` | Provides metadata for analytics and query planning. |

---
```python
#define the sqlalchemy models here
from sqlalchemy import Column, Integer, ForeignKey, String, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "player"
    
    player_id = Column(Integer, primary_key=True, nullable=False)
    gsis_id = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    performances = relationship("Performance", back_populates="player")

    # Many-to-Many relationship through the association table
    teams = relationship("Team", secondary="team_player", back_populates="players")
    
    # Direct access to the link table records (Association Object pattern)
    team_links = relationship("TeamPlayer", back_populates="player", viewonly=True)

class Team(Base):
    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True, nullable=False)
    team_name = Column(String, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"), nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    league = relationship("League", back_populates="teams")
    players = relationship("Player", secondary="team_player", back_populates="teams")
    
    # Direct access to the link table records
    player_links = relationship("TeamPlayer", back_populates="team", viewonly=True)

class Performance(Base):
    __tablename__ = "performance"

    performance_id = Column(Integer, primary_key=True, nullable=False)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"), nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    player = relationship("Player", back_populates="performances")

class League(Base):
    __tablename__ = "league"

    league_id = Column(Integer, primary_key=True, nullable=False)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    teams = relationship("Team", back_populates="league")

class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(Integer, ForeignKey("team.team_id"), primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"), primary_key=True, nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    # We map back to the 'links' attributes to avoid clashing with 'players' and 'teams'
    team = relationship("Team", back_populates="player_links")
    player = relationship("Player", back_populates="team_links")
```
---
## 9.Many -to- Many 
This is **not a simple many-to-many table**.
It is an **association object pattern**.

Why?
- You want **many-to-many** (Team ↔ Player)
- BUT you also want **extra data** about the relationship (`last_changed_date`)
### Why composite primary key?
`primary_key=True on (team_id, player_id)`

This enforces:
- A player **cannot appear twice** in the same team
- `(team_id, player_id)` is **globally unique**

This is your **real uniqueness constraint** in the schema
```python
class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(Integer, ForeignKey("team.team_id"), primary_key=True)
    player_id = Column(Integer, ForeignKey("player.player_id"), primary_key=True)
    last_changed_date = Column(DATETIME, nullable=False)
```

---
## (Many-to-Many Mapping)

```python
teams = relationship(
    "Team",
    secondary="team_player",
    back_populates="players"
)
```
and
```python
players = relationship(
    "Player",
    secondary="team_player",
    back_populates="teams"
)
```
### Concept
This tells SQLAlchemy:

> “To go from Player → Team, use the `team_player` table as a bridge.”

Under the hood:
`Player → team_player → Team`
`Team → team_player → Player`

This allows:
`player.teams`
`team.players`

without manually joining tables.

----
## The `back_populates` vs `backref`

You used `back_populates` in the main tables but `backref` in the `TeamPlayer` table.
### The Concept
These handle **Relationship Symmetry**.
### The Explanation

- **`back_populates`**: Requires you to define the relationship on **both** classes. It is more explicit and considered better for large projects because it's easier to see how tables connect just by looking at the class code.
    
- **`backref`**: Only requires a definition on **one** class. It "automagically" creates the inverse relationship on the other class for you.
---
HTTPX 
HTTPX is a Python HTTP client. It is similar to the very popular requests library, but it supports asynchronous calls, which allows some tasks to finish while others process. The requests library only supports synchronous calls, which wait until they receive a response before continuing. HTTPX is used by pytest to test FastAPI programs.

---
# Study Guide: Pydantic Schemas & DTOs in FastAPI

This guide covers the creation of Pydantic schemas, their role as Data Transfer Objects (DTOs), and how they function as the bridge between your database and the API consumer.

## 1. Core Concepts

### What are Pydantic Schemas?

* **Definition:** Pydantic classes define the structure of the data the API consumer receives.
* **Role:** They act as **Data Transfer Objects (DTOs)**.
* **Purpose:**
* Define a format for transferring data between a producer (Backend) and a consumer (Frontend/Client).
* Decouple the external API format from the internal backend database format.
* Allow the consumer to understand the data structure without knowing backend implementation details.
### Serialization & Deserialization

* **Serialization:** The process of converting Python objects (backend data) into JSON (for HTTP responses).
* **How it works:**
* FastAPI uses Pydantic to automatically serialize data.
* **Pydantic 2** (written in Rust) performs this extremely fast.
* You do *not* need to manage manual JSON conversion in your Python code.
* **OpenAPI Contract:** Pydantic models help auto-generate the `openapi.json` file, creating a standard contract using OpenAPI and JSON Schema standards.
### Important Terminology: "Models"

> **Warning:** Both SQLAlchemy (database layer) and Pydantic (validation/serialization layer) refer to their classes as "models."
> * **SQLAlchemy Models:** Refer to database tables.
> * **Pydantic Schemas:** Refer to the API response structure.
> * *For clarity, this guide refers to Pydantic classes as **Schemas**.*
> 
> 

---
## 2. Implementation Code: `schemas.py`
Below is the complete code for defining the Pydantic schemas.

**Filename:** `schemas.py`

```python
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date

# 1. Performance Schema (Simplest Schema)
# Represents scoring data for a single week.
class Performance(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    performance_id: int
    player_id: int
    week_number: str
    fantasy_points: float
    last_changed_date: date

# 2. PlayerBase Schema (Limited Data)
# Used when nesting player data inside a Team object to avoid massive payloads.
class PlayerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    player_id: int
    gsis_id: str
    first_name: str
    last_name: str
    position: str
    last_changed_date: date

# 3. Player Schema (Full Data)
# Inherits from PlayerBase and ADDS the list of performances.
class Player(PlayerBase):
    model_config = ConfigDict(from_attributes=True)
    performances: List[Performance] = []

# 4. TeamBase Schema (Limited Data)
# Used when nesting team data inside a League object.
class TeamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    team_id: int
    team_name: str
    league_id: int
    last_changed_date: date

# 5. Team Schema (Full Data)
# Inherits from TeamBase and ADDS the list of players (using the limited PlayerBase).
class Team(TeamBase):
    model_config = ConfigDict(from_attributes=True)
    players: List[PlayerBase] = []

# 6. League Schema
class League(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    league_id: int
    league_name: str
    scoring_type: str
    last_changed_date: date
    teams: List[TeamBase] = []

# 7. Counts Schema (Analytics/Special Purpose)
# Does not map directly to a DB table, so no model_config needed.
class Counts(BaseModel):
    league_count: int
    team_count: int
    player_count: int

```

---
## 3. Key Syntax & Design Patterns

### `BaseModel` & `ConfigDict`

* All schemas inherit from `pydantic.BaseModel`.
* **Capabilities:** Provides data validation, type conversion, JSON serialization, and intelligent error handling.
* **`model_config = ConfigDict(from_attributes=True)`:**
* This configuration tells Pydantic to read data even if it comes from a non-dictionary object (specifically, SQLAlchemy ORM objects).
* *Note: In Pydantic v1, this was known as `orm_mode = True`.*

### Syntax Tip: Colons vs. Equals

> **CRITICAL:** Pydantic uses **colons (`:`)** to define types (e.g., `name: str`). SQLAlchemy uses **equals signs (`=`)**. Mixing these up is a frequent source of bugs.

### The "Base" vs. "Full" Pattern (Primary vs. Secondary)
A common strategy is splitting data into "Base" (limited) and "Full" versions to control payload size.

| Schema Pattern | Description | Example |
| --- | --- | --- |
| **Base Schema** | Contains core fields only. Used as a **secondary** schema (nested inside another list). | `PlayerBase` (used inside `Team`) |
| **Full Schema** | Inherits from Base and adds relationships/lists. Used as a **primary** schema (direct API response). | `Player` (used in `/v0/players/`) |

**Why do this?**
When a user requests a `Team`, they want to see the players on that team (`PlayerBase`), but they likely *don't* want a massive list of every single game every player has ever played (`Performance`) included in that same request.

---
## 4. Mapping Schemas to Endpoints
The table below shows which schema is returned (Primary) and which nested schema is included (Secondary) for each endpoint.

| Endpoint URL | Primary Schema (Returned) | Secondary Schema (Nested Attribute) |
| --- | --- | --- |
| `/` | `None` | `None` |
| `/v0/players/` | `Player` | `Performance` |
| `/v0/players/{player_id}/` | `Player` | `Performance` |
| `/v0/performances/` | `Performance` | `None` |
| `/v0/leagues/` | `League` | `TeamBase` |
| `/v0/leagues/{league_id}` | `League` | `TeamBase` |
| `/v0/teams/` | `Team` | `PlayerBase` |
| `/v0/counts/` | `Counts` | `None` |
### The `Counts` Schema

* **Purpose:** Supports analytics (counting leagues, teams, players).
* **Difference:** It is constructed manually in code, not mapped from a database table.
* **Config:** Consequently, it does **not** include the `model_config` line.

---
# Deep Dive: `ConfigDict(from_attributes=True)`
This single line of code is the "magic glue" that allows Pydantic to talk directly to SQLAlchemy. Without it, your API would likely crash when trying to return database results.
## 1. The Fundamental Problem: Dicts vs. Objects
To understand why this config is needed, you have to look at how Python stores data differently in a **Dictionary** versus a **Class Object**.

### Standard Pydantic Behavior (Default)
By default, Pydantic expects to receive a dictionary. It tries to access data using **square brackets** `['key']`.

* **Input Data:** `{'name': 'Tom', 'id': 1}`
* **Pydantic says:** "Give me the value for `['name']`." -> **Success.**

### SQLAlchemy Behavior
SQLAlchemy does *not* return dictionaries. It returns **Instances of Classes** (Python Objects). You access data using **dot notation** `.attribute`.

* **Input Data:** `player_object` (where `player_object.name` is "Tom")
* **Pydantic (Default) says:** "Give me the value for `['name']`."
* **Result:** `TypeError: 'Player' object is not subscriptable` (Crash).

## 2. The Solution: `from_attributes = True`
When you add `model_config = ConfigDict(from_attributes=True)` to your schema, you change how Pydantic retrieves data.

* **Pydantic (with Config) says:** "First, I will try to read this as a dictionary. If that fails (or if it looks like an object), I will try to read it using **dot notation** (`.name`)."

This allows Pydantic to "read" your SQLAlchemy models directly, without you having to manually convert every database row into a dictionary first.

## 3. Visualizing the Interaction
Here is a step-by-step of what happens when you query a Player in FastAPI.
### Step A: SQLAlchemy Query

You run a query like `player = db.query(PlayerModel).first()`.
You get back a Python object that looks like this in memory:

```python
# SQLAlchemy Object (Not a dict!)
<models.Player object at 0x104a>
    .player_id = 99
    .first_name = "Tom"
    .last_name = "Brady"
    # This is a relationship to another table
    .performances = [<models.Performance object>, <models.Performance object>] 

```

### Step B: Pydantic Serialization

You return this object to the `Player` Pydantic schema. Pydantic starts validating:

1. **Field `player_id**`: Pydantic looks at the object. Does `object.player_id` exist? **Yes.** -> Copy value `99`.
2. **Field `first_name**`: Does `object.first_name` exist? **Yes.** -> Copy value `"Tom"`.
3. **Field `performances**`:
* The schema defines this as `List[Performance]`.
* Pydantic sees `object.performances` is a list of SQLAlchemy objects.
* Because `from_attributes=True` is set on the *nested* schema (`Performance`) as well, it recursively converts those objects too!

## 4. Why this is powerful (The "Graph" Traversal)

The real power of `from_attributes=True` is handling **Relationships**.
If you didn't have this, you would have to write code like this for every single endpoint:

```python
# THE HARD WAY (Manual Conversion)
return {
    "player_id": db_player.player_id,
    "first_name": db_player.first_name,
    # You'd have to manually loop through nested lists too!
    "performances": [
        {"week": p.week, "points": p.points} for p in db_player.performances
    ]
}

```

With `from_attributes=True`, you simply write:

```python
# THE EASY WAY
return db_player

```

Pydantic automatically traverses the SQLAlchemy object graph, follows the relationships (like foreign keys), and serializes everything into clean JSON.
### Summary
* **Default Pydantic:** Expects `data['key']`.
* **SQLAlchemy:** Provides `data.key`.
* **`from_attributes=True`:** Tells Pydantic to use `data.key` (getattr) instead of `data['key']` (getitem), enabling automatic conversion of database objects to JSON.

---
### FastAPI Controller (main.py)

```python
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

The second parameter of the decorator is response_model=list[schemas.Player]) . This informs FastAPI that the data returned from this endpoint will be a list of Pydantic Player objects, as defined in the schemas.py file. This information will be included in the OpenAPI specification that FastAPI automatically creates for this API. Consumers can count on the returned data being valid according to this definition.
```python
@app.get("/v0/players/", response_model = list[schemas.Player])
def read_players(skip:int = 0, limit:int = 100,
                 min_last_changed_date: date = None,
                 first_name: str = None, last_name: str = None,
                 db:Session = Depends(get_db)):
    players = crud.get_players(db,skip = skip, limit = limit,
                               min_last_changed_date = min_last_changed_date,
                               first_name = first_name,
                               last_name = last_name)
    return players
```

FastAPI will automatically include these parameters as query parameters in the API definition. Query parameters are included in the URL path with a question mark in front and an ampersand between. For instance, to call this query method, the API consumer could use this request: HTTP verb: GET URL: {base URL}/v0/players/?first_name=Bryce&last_name=Young

---
## Core Concepts
### 1. FastAPI TestClient

The `TestClient` is a tool provided by FastAPI (built on top of the `httpx` library) that allows you to simulate HTTP requests without actually running a live server. It triggers the FastAPI application logic internally, making tests fast and reliable.

### 2. Assertions
In testing, an **assertion** is a check to see if a condition is true. If the condition is false (e.g., the status code is 404 instead of 200), the test fails.

* `response.status_code`: Checks if the HTTP request was successful.
* `response.json()`: Parses the response body into a Python dictionary or list.

### 3. Path Parameters and Query Parameters
The code tests two ways of sending data to an API:

* **Path Parameters:** `/v0/players/1001/` (targeting a specific resource ID).
* **Query Parameters:** `/v0/players/?skip=0&limit=2000` (used for filtering or pagination).

---
## Code Snippet Explanations

### A. Initialization

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

```

* **Explanation:** You import your FastAPI instance (`app`) and wrap it in `TestClient`. The `client` object is now your "virtual browser" that can perform `.get()`, `.post()`, etc.

---
### B. Testing List Endpoints (Pagination)

```python
def test_read_players():
    response = client.get("/v0/players/?skip=0&limit=2000")

    assert response.status_code == 200
    assert len(response.json()) == 1018

```

* **Logic:** This sends a GET request to the players list.
* **Goal:** It verifies that the database contains exactly **1018** players when the limit is set high enough to fetch them all.

---
### C. Testing Specific Resource Retrieval

```python
def test_read_players_with_id():
    response = client.get("/v0/players/1001/")

    assert response.status_code == 200
    assert response.json().get("player_id") == 1001

```

* **Logic:** Requests a single player by their ID (`1001`).
* **Goal:** It ensures that the API returns the correct object and that the `player_id` in the JSON body matches the one requested in the URL.

---
### D. Testing Nested Data Relationships

```python
def test_read_leagues_with_id():
    response = client.get("/v0/leagues/5002/")
    assert response.status_code == 200
    assert len(response.json()["teams"]) == 8

```

* **Logic:** Fetches a league and looks inside the `teams` key.
* **Goal:** This validates **relationships**. It confirms that league `5002` correctly has **8** teams associated with it in the database schema.

---
### E. Testing Aggregated Data (Counts)

```python
def test_counts():
    response = client.get("/v0/counts/")

    assert response.status_code == 200
    assert response.json()["league_count"] == 5
    assert response.json()["team_count"] == 20

```

* **Logic:** Calls a summary endpoint.
* **Goal:** Verifies that the "stats" or "summary" logic of the API is calculating totals correctly (e.g., that there are exactly 5 leagues and 20 teams in the system).

---
## Summary of Expected Data Structure

| Endpoint | Test Goal | Expected Result |
| --- | --- | --- |
| `/` | Health Check | Status 200, "API health check successful" |
| `/v0/players/` | Bulk Fetch | 1018 items returned |
| `/v0/leagues/5002/` | Relationship Check | Must contain a list of 8 teams |
| `/v0/counts/` | Data Integrity | Checks total counts of Leagus, Teams, and Players |

----
#### Docker
```python
FROM python:3.10-slim

#set Docker work directory
WORKDIR /code
#This statement sets a working directory inside the container image. 
#This working directory is where the remaining commands will be executed unless otherwise specified

#copy from the build context directory to the docker
COPY requirements.txt /code
#This copies the requirements.txt file from context, which is a set of files in a location that you will specify when you execute the build statement.

#Install the python libraries
RUN pip install --no-cache-dir --upgrade -r requirements.txt
#This uses pip to install the specified libraries in your requirements.txt file into a new layer in the Docker image. A Docker container image is like a brand-new virtual server: you have complete control of the libraries and versions that are contained in it so that your application works correctly.

#Copy the code files and database from the build context directory to the docker
COPY *.py /code/
COPY *.db /code/
#These two statements copy your Python program files and SQLite database from the context directory to your Docker working directory.

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","8080","--reload"]
```

These are all the instructions you need to define your container image. The next step will be to build the container image in your local repository.

```python
docker --version
docker build -t apicontainerimage .
docker images
docker run --publish 8080:8080 --name apicontainer apicontainerimage
```

---
# Deploying to AWS

This guide walks you through deploying your Docker container using **Amazon Lightsail**, one of the simplest ways to get started with AWS.

---
## 1. Setting Up Your AWS Account

To begin, create a new AWS account and store your login credentials securely.

* **Root User:** For this project, it is acceptable to use the root user account (identified by your email).
* **Security:** You **must** enable Multi-Factor Authentication (MFA) by following the directions in the *AWS Identity and Access Management (IAM) User Guide*.
* **Best Practice:** If you continue using AWS, create a separate administration account for daily work instead of using the root account.

---
## 2. Creating a Lightsail Container Service

1. Log in to the [AWS Console](https://console.aws.amazon.com/).
2. Search for **Lightsail** in the top search bar.
3. Select **Containers** from the left-hand menu.
4. Click **"Create container service."**

### Configuration Details:

* **Region:** Select the region nearest to you for the best performance.
* **Power:** Choose **Nano** or **Micro**.
* **Scale:** Choose **1**.
* **Identify your service:** Choose a name (e.g., `aws-api-container`).

Click **"Create container service."** It will take several minutes for the status to update to ready.

---
## 3. Installing Required Tools

### AWS CLI

You need the AWS CLI to interact with your account via the terminal. Follow the official AWS instructions to install or update it. Verify the installation:

```bash
aws --version

```

### Lightsail Control Plug-in

Lightsail requires an additional plugin to manage containers. Follow the AWS documentation to install the **Amazon Lightsail container services plug-in**.

---
## 4. Configuring Login Credentials

Configure your authentication to connect the CLI to your account.

> [!WARNING]
> Be extremely careful with your credentials. Never commit them to a source code repository (like GitHub).

Run the following command to verify your configuration:

```bash
aws sts get-caller-identity

```

You should receive a JSON response containing your `UserId`, `Account`, and `Arn`.

---
## 5. Pushing Your Container Image to Lightsail

Verify that your Docker image exists locally:

```bash
docker images

```

To push the image, use the following command structure (ensure you replace the placeholders with your specific details):

```bash
aws lightsail push-container-image --region [YOUR_REGION] --service-name aws-api-container --label aws-api --image [LOCAL_IMAGE_NAME]:[TAG]

```

**Example:**

```bash
aws lightsail push-container-image --region us-east-1 --service-name aws-api-container --label aws-api --image apicontainerimage:latest

```

Once finished, the terminal will provide a reference string like: ` :aws-api-container.aws-api.1`. You can also view this in the **Images** tab of your Lightsail console.

---
## 6. Creating a Lightsail Deployment

Now that the image is stored in AWS, you must deploy it.

1. Navigate to the **Deployments** tab of your service.
2. Select **"Create your first deployment."**
3. **Container name:** Choose a unique name (e.g., `aws-api-container-1`).
4. **Image:** Select the stored image you just pushed.
5. **Ports:** Click **"+ Add open ports"** and enter **80**.
6. **Public Endpoint:** In the drop-down box, select the container name you just defined.
7. Click **"Save and deploy."**

---
## 7. Verification

After a few minutes, the status will change to **Active**.

* Find the **"Public domain"** URL generated in the dashboard.
* Copy and paste this URL into your browser.
* If successful, you will see your API’s health check page.

**Congratulations! Your API is now live on AWS.**
