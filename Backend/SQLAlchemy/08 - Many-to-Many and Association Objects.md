---
tags: [sqlalchemy, orm, many-to-many, association-object, secondary, composite-primary-key, back_populates, backref]
aliases: [Many-to-many, Association object, secondary=, TeamPlayer, Composite primary key, back_populates vs backref]
---

# 08 — Many-to-Many and Association Objects

> [!info] Source
> Your own notes (section 9 of the old file), expanded. Back to [[00 - Index]] · Previous: [[07 - Relationships One-to-Many]]

## The one-sentence version

Many-to-many needs a **link table**; if the link table only holds the two FKs use `relationship(secondary=...)`, and if it needs **extra columns** (dates, roles…) make the link table a real model — the **association object pattern**.

## The example: Team ↔ Player

A player can be on many teams; a team has many players. And you want to record **when** each membership last changed (`last_changed_date`).

That extra column is why this is **not** a simple many-to-many table — it's an **association object**.

## Step 1 — the link table as a model

```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(Integer, ForeignKey("team.team_id"), primary_key=True)
    player_id = Column(Integer, ForeignKey("player.player_id"), primary_key=True)
    last_changed_date = Column(DateTime, nullable=False)
```

### Why a composite primary key?

`primary_key=True` on **both** `team_id` and `player_id` makes the pair `(team_id, player_id)` the primary key. This enforces:

- a player **cannot appear twice** in the same team,
- the pair is **globally unique** in the table.

That is your real uniqueness constraint, expressed in the schema rather than in application code. (A surrogate `id` column plus `UniqueConstraint("team_id", "player_id")` is the alternative; composite PK is simpler when you don't need to reference link rows elsewhere.)

## Step 2 — the many-to-many mapping on the main tables

```python
class Team(Base):
    __tablename__ = "team"
    team_id = Column(Integer, primary_key=True)
    name = Column(String)

    players = relationship(
        "Player",
        secondary="team_player",
        back_populates="teams",
    )

class Player(Base):
    __tablename__ = "player"
    player_id = Column(Integer, primary_key=True)
    name = Column(String)

    teams = relationship(
        "Team",
        secondary="team_player",
        back_populates="players",
    )
```

### What `secondary=` means

> "To go from Player → Team, use the `team_player` table as a bridge."

Under the hood:

```
Player -> team_player -> Team
Team   -> team_player -> Player
```

So you get `player.teams` and `team.players` without writing the joins yourself. `secondary` accepts the table **name** as a string (resolved from `Base.metadata`) or the `Table` object.

## Step 3 — (optional) navigate the association rows themselves

If you need to read `last_changed_date`, add relationships **to** `TeamPlayer`:

```python
class TeamPlayer(Base):
    ...
    team = relationship("Team", back_populates="memberships")
    player = relationship("Player", back_populates="memberships")

class Team(Base):
    ...
    memberships = relationship("TeamPlayer", back_populates="team")

class Player(Base):
    ...
    memberships = relationship("TeamPlayer", back_populates="player")
```

Now:

```python
for m in team.memberships:
    print(m.player.name, m.last_changed_date)
```

> [!warning] Don't write through both paths
> If you have both `Team.players` (via `secondary`) **and** `Team.memberships` (via the association object), SQLAlchemy will warn about conflicting writes. Read via either; **write via the association object only** (create `TeamPlayer(team=t, player=p, last_changed_date=now)`), or mark the `secondary` relationship `viewonly=True`.

## Creating links

```python
from datetime import datetime, timezone

# simple (only when the link table has NO extra required columns)
team.players.append(player)

# association object (required when extra columns exist)
db.add(TeamPlayer(team_id=team.team_id, player_id=player.player_id,
                  last_changed_date=datetime.now(timezone.utc)))
db.commit()
```

With `last_changed_date` being `nullable=False`, `team.players.append(player)` would fail — SQLAlchemy doesn't know what to put in that column. Hence the association-object insert.

## Plain many-to-many (no extra columns) for comparison

```python
from sqlalchemy import Table

team_player = Table(
    "team_player", Base.metadata,
    Column("team_id", ForeignKey("team.team_id"), primary_key=True),
    Column("player_id", ForeignKey("player.player_id"), primary_key=True),
)

class Team(Base):
    ...
    players = relationship("Player", secondary=team_player, back_populates="teams")
```

No class for the link table, and `team.players.append(p)` just works.

## back_populates vs backref

Both handle **relationship symmetry** — making sure `a.bs` and `b.a` stay in sync.

| | `back_populates` | `backref` |
|---|---|---|
| Where you write it | On **both** classes, each naming the other's attribute | On **one** class only |
| The other side | You define it explicitly | Created automatically ("automagically") |
| Readability | You can see every link by reading the class | The inverse attribute is invisible in the other class's source |
| Recommended | **Yes** — explicit, better for large projects, required style in 2.x typed models | Legacy convenience |

```python
# back_populates (explicit, both sides)
class User(Base):
    products = relationship("Product", back_populates="owner")
class Product(Base):
    owner = relationship("User", back_populates="products")

# backref (one side; Product.owner is generated)
class User(Base):
    products = relationship("Product", backref="owner")
```

If you mixed them in one model file (main tables with `back_populates`, `TeamPlayer` with `backref`), it works, but pick one style — `back_populates` — for consistency.

## Next

→ [[09 - Querying Data]]
