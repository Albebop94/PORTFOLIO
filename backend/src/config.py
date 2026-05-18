from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Backend DDD Portfolio"
    database_url: str = "sqlite+aiosqlite:///./portfolio.db"

    model_config = {"env_file": ".env"}


settings = Settings()
