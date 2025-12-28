from typing import Set, Optional, Literal
from pydantic import BaseModel, Field, ValidationError
import os


# Application-level config
class AppConfig(BaseModel):
    env: str = Field(default="dev")
    service_name: str = Field(default="rate-limited-api")
    log_level: str = Field(default="INFO")
    

# Rate limiting config
class RateLimitConfig(BaseModel):
    requests_per_window: int = Field(..., gt=0)
    window_seconds: int = Field(..., gt=0)
    allowed_api_keys: Set[str] = Field(..., min_length=1)


# State backend config
class StateConfig(BaseModel):
    backend: Literal["memory", "file"]
    file_path: Optional[str] = None    
    
    def validate_backend(self) -> None:
        if self.backend == "file" and not self.file_path:
            raise ValueError("file_path must be set when backend store is 'file'")
        

# Root settings object
class Settings(BaseModel):
    app: AppConfig
    rate_limit: RateLimitConfig
    state: StateConfig


# Config loader
def load_settings() -> Settings:
    try:
        settings = Settings(
            app=AppConfig(
                env=os.getenv("APP_ENV", "dev"),
                service_name=os.getenv("SERVICE_NAME", "rate-limited-api"),
                log_level=os.getenv("LOG_LEVEL", "INFO"),
            ),
            rate_limit=RateLimitConfig(
                requests_per_window=int(os.environ["REQUESTS_PER_WINDOW"]),
                window_seconds=int(os.environ["WINDOW_SECONDS"]),
                allowed_api_keys=set(
                    key.strip()
                    for key in os.environ["ALLOWED_API_KEYS"].split(",")
                ),
            ),
            state=StateConfig(
                backend=os.getenv("STATE_BACKEND", "memory"),
                file_path=os.getenv("STATE_FILE_PATH"),
            ),
        )        
        settings.state.validate_backend()
        return settings    
    except KeyError as exc:
        raise RuntimeError(f"Missing required environment variable: {exc}") from exc
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc
