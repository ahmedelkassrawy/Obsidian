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