from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://titanbay:titanbay@localhost:5432/titanbay"


settings = Settings()