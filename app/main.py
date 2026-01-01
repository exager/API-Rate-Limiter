from fastapi import FastAPI
from utils.config import load_settings
from utils.logging import configure_logging
from core.rate_limiter import RateLimiter
from stores.memory_store import InMemoryRateLimitStore
from stores.file_store import FileRateLimitStore
from api.routes import router
from api.dependencies import set_rate_limiter


settings = load_settings()

configure_logging(settings.app.log_level)

# Choose state backend
if settings.state.backend == "memory":
    store = InMemoryRateLimitStore()
elif settings.state.backend == "file":
    store = FileRateLimitStore(settings.state.file_path)
else:
    raise RuntimeError(f"Unsupported state backend: {settings.state.backend}")

rate_limiter = RateLimiter(
    config=settings.rate_limit,
    store=store,
)
set_rate_limiter(rate_limiter)

app = FastAPI(title=settings.app.service_name)
app.include_router(router)