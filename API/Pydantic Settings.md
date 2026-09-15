---
description: "A pasted config.py snippet showing pydantic-settings BaseSettings reading values from a .env file."
domain: backend
type: reference
status: raw
tags:
  - domain/backend
  - type/reference
  - status/raw
  - topic/pydantic
  - topic/fastapi
aliases:
  - "BaseSettings"
  - "env file config"
hubs:
  - "[[Pydantic]]"
  - "[[FastAPI]]"
---
config.py
```python
from pydantic_settings import BaseSettings
from pydantic import Extra
from typing import List

class Settings(BaseSettings):
    GOOGLE_API_KEY : str

    class Config:
        env_file = ".env"
        env_prefix = ""  # Add this line to remove any prefix for environment variables

def get_settings() -> Settings:
    return Settings()
```