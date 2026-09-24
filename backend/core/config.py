from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Offline AI Assistant"
    API_V1_STR: str = "/api/v1"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "qwen3:4b"
    
    # We will just accept the user's string
    
    class Config:
        env_file = ".env"

settings = Settings()
