import os
from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@db:5432/app")
    model_config = {"env_file": ".env", "case_sensitive": False}

settings = Settings()
engine = create_engine(settings.database_url, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
