from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.config import load_settings
from utils.logging import configure_logging
from app import app_states
from core.rate_limiter import RateLimiter
from stores.memory_store import InMemoryRateLimitStore
from stores.file_store import FileRateLimitStore
from api.routes import router
from api.debug_routes import router as debug_router
from pathlib import Path

app = FastAPI()

@app.on_event("startup")
def startup_event():
    app_states.settings = load_settings()
    configure_logging(app_states.settings.app.log_level)
    # Choose state backend
    if app_states.settings.state.backend == "memory":
        app_states.store = InMemoryRateLimitStore()
    elif app_states.settings.state.backend == "file":
        app_states.store = FileRateLimitStore(app_states.settings.state.file_path)
    else:
        raise RuntimeError(f"Unsupported state backend: {app_states.settings.state.backend}")

    app_states.rate_limiter = RateLimiter(
        app_states.settings.rate_limit,
        app_states.store,
    )
    app.title = app_states.settings.app.service_name


app.include_router(router)
app.include_router(debug_router)    