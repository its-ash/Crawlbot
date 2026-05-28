from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    google_api_key: Optional[str] = None
    google_cse_id: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    database_url: str = "sqlite:///./crawlbot.db"
    max_concurrent_agents: int = 10
    results_per_search: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()
