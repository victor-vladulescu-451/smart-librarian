from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    OPENAI_API_KEY: str | None = None
    CHROMA_DIR: str = "./chroma_data"
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
