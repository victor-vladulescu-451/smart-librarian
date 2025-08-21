from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # env
    ENV: str = "dev"
    OPENAI_API_KEY: str | None = None
    # Vector store
    CHROMA_DIR: str = "./chroma_data"
    CHROMA_COLLECTION: str = "books"
    # scalable option
    TITLES_PAGE_SIZE: int = 500
    # Optional: normalized title key used at ingest for case-insensitive exact match
    TITLE_NORM_KEY: str = "title_norm"
    # backend
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
