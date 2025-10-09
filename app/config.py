from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    allowed_origins: List[str] = ["*"]      # CSV in env: "https://foo.com,https://bar.com"
    log_level: str = "info"                 # info | warning | error | debug
    uvicorn_workers: int = 2

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _split_csv(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
