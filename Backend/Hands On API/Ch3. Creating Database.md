![[Pasted image 20260915145445.png]]

## The Three Layers

- **Data transfer and validation** — Pydantic.
- **API controller** — FastAPI. It handles all the processing of the API along with other functions.
- **Database classes** — SQLAlchemy. These classes handle querying the database, and you deploy them along with your API code.

## The Files You Will Create

| Filename | Purpose |
| --- | --- |
| `models.py` | Defines the SQLAlchemy classes for the database tables |
| `database.py` | Configures SQLAlchemy to use the SQLite database |
| `crud.py` | Helper functions to query the database |
| `requirements.txt` | Installs specific versions of libraries with pip |
| `test_crud.py` | The pytest file to unit-test your SQLAlchemy code |

## Creating the Models File

Create a file named `models.py` with the following contents:

```python
# models.py
"""SQLAlchemy models"""
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from database import Base


class Player(Base):
    __tablename__ = "player"

    player_id = Column(Integer, primary_key=True, index=True)
    gsis_id = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    performances = relationship("Performance", back_populates="player")

    # Many-to-many relationship between Player and Team
    teams = relationship(
        "Team", secondary="team_player", back_populates="players"
    )


class Performance(Base):
    __tablename__ = "performance"

    performance_id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Float, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"))

    player = relationship("Player", back_populates="performances")


class League(Base):
    __tablename__ = "league"

    league_id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"))

    league = relationship("League", back_populates="teams")
    players = relationship(
        "Player", secondary="team_player", back_populates="teams"
    )


class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(
        Integer, ForeignKey("team.team_id"), primary_key=True, index=True
    )
    player_id = Column(
        Integer, ForeignKey("player.player_id"), primary_key=True, index=True
    )
    last_changed_date = Column(Date, nullable=False)
```

### Imports

At the top of most Python files you find import statements. The power of the Python ecosystem comes from the variety of external libraries you can use.

You import SQLAlchemy's `relationship` functionality, which enables foreign key relationships between tables.

The `database` import refers to the `database.py` file with the SQLAlchemy configuration. You use the `Base` class, a standard template you'll use for the classes in `models.py`.

### The Player Class

Now you define the `Player` class, the Python class you'll use to store data from the SQLite `player` table.

The `class` statement names the class and specifies that it is a subclass of the `Base` template imported from `database.py`. The `__tablename__` magic command tells SQLAlchemy to reference the `player` table.

Because of this, when you ask SQLAlchemy to query `Player`, it knows behind the scenes to access the `player` table. This is one of the key benefits of an ORM — mapping the Python code automatically to the underlying database.

```python
class Player(Base):
    __tablename__ = "player"
```

The rest of the class maps additional details about the table. Each statement defines one attribute using the `Column` method:

```python
player_id = Column(Integer, primary_key=True, index=True)
gsis_id = Column(String, nullable=True)
first_name = Column(String, nullable=False)
last_name = Column(String, nullable=False)
position = Column(String, nullable=False)
last_changed_date = Column(Date, nullable=False)
```

A few things to notice:

- The attribute names are automatically matched to the column names in the database.
- The data types (`String`, `Integer`) are SQLAlchemy data types from your import statement.
- The `primary_key` definition gives you query optimization, uniqueness enforcement, and relationships between classes.

### Relationships

You define the foreign key relationship between tables with the `relationship()` function. This gives you a `Player.performances` attribute that returns all related rows from the `performance` table for each row in the `player` table.

There is another kind of relationship that uses the `team_player` association table to connect `player` to `team`. By defining `secondary="team_player"`, this relationship gives a `Player` record a `Player.teams` attribute. This is the many-to-many relationship discussed when creating the database tables.

### The Performance Class

```python
class Performance(Base):
    __tablename__ = "performance"

    performance_id = Column(Integer, primary_key=True, index=True)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Float, nullable=False)
    last_changed_date = Column(Date, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"))

    player = relationship("Player", back_populates="performances")
```

This class has a `player` relationship that is the mirror image of the `performances` relationship in the `player` table.

Looking at the two together, the `back_populates` statement in one refers to the variable assigned in the other. Together they create a two-way relationship between the parent (`player`) and the child (`performance`).

### The League Class

```python
class League(Base):
    __tablename__ = "league"

    league_id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(Date, nullable=False)

    teams = relationship("Team", back_populates="league")
```

`League` is the topmost parent class in your code, as shown in Figure 3-2. The `teams` relationship enables `League.teams` and has a matching relationship in the `Team` class.

### The Team Class

```python
class Team(Base):
    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"))

    league = relationship("League", back_populates="teams")
    players = relationship(
        "Player", secondary="team_player", back_populates="teams"
    )
```

This class has matching relationships to connect with the `league` table and, indirectly, the `player` table.

### The TeamPlayer Class

```python
class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(
        Integer, ForeignKey("team.team_id"), primary_key=True, index=True
    )
    player_id = Column(
        Integer, ForeignKey("player.player_id"), primary_key=True, index=True
    )
    last_changed_date = Column(Date, nullable=False)
```

The `TeamPlayer` class has no relationships, because those are defined on the `Team` and `Player` classes.

You have now defined all the SQLAlchemy models. Excellent progress.

## Creating the Database Configuration File

Next, `database.py` sets up the SQLAlchemy configuration to connect to the SQLite database, along with other Python objects you'll use for database work.

The tasks in this file are:

- Create a database connection that points to the SQLite database with the correct settings.
- Create a parent class you'll use to define the Python table classes.

Create a file with the following contents, and name it `database.py`:

```python
# database.py
"""Database configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./fantasy_data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

Take this file piece by piece.

### Imports

Three specific functions are imported from SQLAlchemy. You could import the whole library at once, but importing specific functions limits possible conflicts between duplicate function names across libraries:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
```

### Getting the Session

The next three steps work together to get the session — the SQLAlchemy object that manages the conversation with the database.

First, create a database URL that tells SQLAlchemy the database type (SQLite) and where to find the file (the same folder as this file, named `fantasy_data.db`):

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./fantasy_data.db"
```

Then create an `engine` object. The one configuration setting here allows multiple connections to the database without throwing an error:

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
```

Use the engine to create a session named `SessionLocal` with a couple more settings:

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### The Base Class

The last command creates a `Base` class. This is the standard template SQLAlchemy provides for the models you create in `models.py`:

```python
Base = declarative_base()
```

## Creating SQLAlchemy Helper Functions

The files so far give you a connection to the database and classes that represent tables. Next you create `crud.py`, which contains the query functions. The name stands for Create, Read, Update, Delete (CRUD).

Create a file with the following contents, and name it `crud.py`:

```python
# crud.py
"""SQLAlchemy Query Functions"""
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date

import models


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(
        models.Player.player_id == player_id
    ).first()


def get_players(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_last_changed_date: date = None,
    last_name: str = None,
    first_name: str = None,
):
    query = db.query(models.Player)
    if min_last_changed_date:
        query = query.filter(
            models.Player.last_changed_date >= min_last_changed_date
        )
    if first_name:
        query = query.filter(models.Player.first_name == first_name)
    if last_name:
        query = query.filter(models.Player.last_name == last_name)
    return query.offset(skip).limit(limit).all()


def get_performances(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_last_changed_date: date = None,
):
    query = db.query(models.Performance)
    if min_last_changed_date:
        query = query.filter(
            models.Performance.last_changed_date >= min_last_changed_date
        )
    return query.offset(skip).limit(limit).all()


def get_league(db: Session, league_id: int = None):
    return db.query(models.League).filter(
        models.League.league_id == league_id
    ).first()


def get_leagues(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_last_changed_date: date = None,
    league_name: str = None,
):
    query = db.query(models.League).options(
        joinedload(models.League.teams)
    )
    if min_last_changed_date:
        query = query.filter(
            models.League.last_changed_date >= min_last_changed_date
        )
    if league_name:
        query = query.filter(models.League.league_name == league_name)
    return query.offset(skip).limit(limit).all()


def get_teams(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_last_changed_date: date = None,
    team_name: str = None,
    league_id: int = None,
):
    query = db.query(models.Team)
    if min_last_changed_date:
        query = query.filter(
            models.Team.last_changed_date >= min_last_changed_date
        )
    if team_name:
        query = query.filter(models.Team.team_name == team_name)
    if league_id:
        query = query.filter(models.Team.league_id == league_id)
    return query.offset(skip).limit(limit).all()


# analytics queries
def get_player_count(db: Session):
    query = db.query(models.Player)
    return query.count()


def get_team_count(db: Session):
    query = db.query(models.Team)
    return query.count()


def get_league_count(db: Session):
    query = db.query(models.League)
    return query.count()
```

### Imports

```python
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from datetime import date

import models
```

`Session` and `joinedload` are used by the query functions. `date` is an important data type that lets you filter by date. The `import models` line lets you reference the model file you created.

These functions reference the classes in `models.py` and use SQLAlchemy built-in functions to retrieve data with prepared SQL statements.

### get_player

```python
def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(
        models.Player.player_id == player_id
    ).first()
```

The parameters are a database session (used to connect to the database) and a specific `player_id`. Using `filter(models.Player.player_id == player_id).first()`, this function looks up a specific `Player.player_id` and returns the first matching instance.

Because `player_id` is a primary key in `models.py` and in the SQLite database, this query returns a single result.

### get_players

The next function adds several new parameters:

```python
def get_players(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_last_changed_date: date = None,
    last_name: str = None,
    first_name: str = None,
):
```

- `skip` and `limit` are for pagination, which lets the user request records in chunks rather than the full list.
- `min_last_changed_date` excludes records older than a given date.
- `skip` defaults to `0` and `limit` defaults to `100`. If they aren't passed, those defaults apply.
- `min_last_changed_date`, `first_name`, and `last_name` have no default, so they default to `None`.

The body uses the queries to filter results:

```python
query = db.query(models.Player)
if min_last_changed_date:
    query = query.filter(
        models.Player.last_changed_date >= min_last_changed_date
    )
if first_name:
    query = query.filter(models.Player.first_name == first_name)
if last_name:
    query = query.filter(models.Player.last_name == last_name)
```

The last statement applies the `skip` and `limit` parameters:

```python
return query.offset(skip).limit(limit).all()
```

This grabs a specific chunk of records. `skip` tells the query to skip a number of records from the beginning; `limit` returns only a set number.

For example, a user might skip `0` and limit `20` to get the first 20 records. They could call it again with skip `20` and limit `20` to get the next 20.

### get_leagues

This function uses a new statement, so it's worth a closer look:

```python
def get_leagues(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_last_changed_date: date = None,
    league_name: str = None,
):
    query = db.query(models.League).options(
        joinedload(models.League.teams)
    )
    if min_last_changed_date:
        query = query.filter(
            models.League.last_changed_date >= min_last_changed_date
        )
    if league_name:
        query = query.filter(models.League.league_name == league_name)
    return query.offset(skip).limit(limit).all()
```

It uses `.options(joinedload(models.League.teams))`. This is a type of eager loading: SQLAlchemy retrieves the joined team data at the same time it retrieves the league data.

### Analytics Queries

The final set of queries support AI and large language models, based on the recommendation to provide a separate endpoint for analytics questions. These endpoints provide counts for players, leagues, and teams.

This helps the AI use the pagination functions and answer questions about record counts without making large API calls:

```python
# analytics queries
def get_player_count(db: Session):
    query = db.query(models.Player)
    return query.count()


def get_team_count(db: Session):
    query = db.query(models.Team)
    return query.count()


def get_league_count(db: Session):
    query = db.query(models.League)
    return query.count()
```

You have created all the SQLAlchemy classes and helper functions. Since every function in `crud.py` reads data, you have only implemented the "R" in CRUD. That's fine — all your user stories require read-only functionality.

If you were building an API that allowed creating, updating, or deleting records, this file could be extended with more functions. Now it's time to unit-test these queries with pytest.

## Installing pytest in Your Environment

Now that the database code is written, you're ready to test it with pytest.

First, add an entry for pytest to `requirements.txt`. The updated file should look like this:

```text
SQLAlchemy>=2.0.0
Pytest>=8.1.0
```

To install pytest, run the install command again:

```bash
pip3 install -r requirements.txt
```

You should see a message that pytest 8.1.0 or higher was successfully installed or was "already satisfied."

To verify the installation, run `pip3 show Pytest`. You'll see a confirmation similar to this:

```text
$ pip3 show Pytest
Name: pytest
Version: 8.1.1
Summary: pytest: simple powerful testing with Python
Home-page:
Author: Holger Krekel, Bruno Oliveira, Ronny Pfannschmidt, Floris Bruhin, Others (See AUTHORS)
Author-email:
License: MIT
```

## Testing Your SQLAlchemy Code

pytest is simple to use, with a couple of naming conventions it expects:

- Any file containing tests must start with `test_` or end with `_test`.
- Inside the test file, pytest runs any function whose name begins with `test`.
- Inside a test function, you include an `assert` statement. If it's true, the flow continues; if all assertions are true, the test passes. If an assertion is false, the code raises an `AssertionError` and the test fails.

Your unit tests are basic: they check that the row counts returned by your SQLAlchemy code match the values you checked earlier with SQL queries.

Create a file named `test_crud.py` with the following contents:

```python
# test_crud.py
"""Testing SQLAlchemy Helper Functions"""
import pytest
from datetime import date

import crud
from database import SessionLocal

# use a test date of 4/1/2024 to test the min_last_changed_date filter
test_date = date(2024, 4, 1)


@pytest.fixture(scope="function")
def db_session():
    """This starts a database session and closes it when done"""
    session = SessionLocal()
    yield session
    session.close()


def test_get_player(db_session):
    """Tests you can get the first player"""
    player = crud.get_player(db_session, player_id=1001)
    assert player.player_id == 1001


def test_get_players(db_session):
    """Tests that the count of players in the database is what is expected"""
    players = crud.get_players(
        db_session, skip=0, limit=10000, min_last_changed_date=test_date
    )
    assert len(players) == 1018


def test_get_players_by_name(db_session):
    """Tests that filtering players by name returns the expected player"""
    players = crud.get_players(db_session, first_name="Bryce")
    assert len(players) == 1
    assert players[0].player_id == 2009


def test_get_all_performances(db_session):
    """Tests that the count of performances is what is expected - all of them"""
    performances = crud.get_performances(db_session, skip=0, limit=100000)
    assert len(performances) == 17306


def test_get_new_performances(db_session):
    """Tests that the count of recent performances is what is expected"""
    performances = crud.get_performances(
        db_session, skip=0, limit=100000, min_last_changed_date=test_date
    )
    assert len(performances) == 2711


# test the count functions
def test_get_player_count(db_session):
    player_count = crud.get_player_count(db_session)
    assert player_count == 1018
```

### How This File Follows pytest Conventions

The file is named `test_crud.py`, so pytest recognizes it as a test file automatically. It contains six functions beginning with `test_`, which run when the file executes. Each ends with an `assert` statement.

### The Fixture

The first function needs some explanation. Above it is the decorator `@pytest.fixture(scope="function")`. A fixture is used during the arrange phase, which prepares the testing setup. This fixture uses function scope, so it runs once for each test function:

```python
@pytest.fixture(scope="function")
```

The body of `db_session()` creates a database session, pauses while the test function uses it (through `yield`), and closes the session when the test completes:

```python
def db_session():
    """This starts a database session and closes it when done"""
    session = SessionLocal()
    yield session
    session.close()
```

### Verifying the Date-Based Queries

To verify the date-based queries work, the performance tests check the full results and then the results limited by `last_changed_date`.

Remember the earlier SQL queries returned these results for the `performance` table:

```sql
sqlite> select count(*) from performance;
17306
sqlite> select count(*) from performance where last_changed_date >= '2024-04-01';
2711
```

To verify the first result, this function has no date parameter:

```python
def test_get_all_performances(db_session):
    """Tests that the count of performances is what is expected - all of them"""
    performances = crud.get_performances(db_session, skip=0, limit=100000)
    assert len(performances) == 17306
```

To verify the second result, the next function uses a `last_changed_date` of `2024-04-01`, set in the `test_date` variable at the top of the file. That date matches 2,711 records:

```python
def test_get_new_performances(db_session):
    """Tests that the count of recent performances is what is expected"""
    performances = crud.get_performances(
        db_session, skip=0, limit=100000, min_last_changed_date=test_date
    )
    assert len(performances) == 2711
```

The last test verifies one of the analytics queries:

```python
def test_get_player_count(db_session):
    player_count = crud.get_player_count(db_session)
    assert player_count == 1018
```

### Running the Tests

To run the tests, enter `pytest test_crud.py`. You should see output similar to this:

```text
$ pytest test_crud.py
================== test session starts ======================
platform linux -- Python 3.10.13, pytest-8.1.2, pluggy-1.5.0
rootdir: /workspaces/adding-more-data/chapter3
plugins: anyio-4.4.0
collected 5 items

test_crud.py .....                                     [100%]

=================== 5 passed in 0.22s =======================
```

You have verified that your SQLAlchemy classes and helper functions work correctly. The database work is done.
