# Rate Limiter API (FastAPI)

This project is a small but production-oriented FastAPI service that demonstrates how to implement API rate limiting with clean architecture, configuration-driven behavior, and proper lifecycle management.

The goal is not to build a feature-heavy product, but to show how a backend service should be structured, configured, tested, and run in real-world scenarios.

## What this service does

- Exposes a simple API endpoint protected by a rate limiter  
- Limits requests per API key within a configurable time window  
- Supports multiple state backends:
  - In-memory (for local development and CI)
  - File-based (to demonstrate persistence across restarts)
- Provides a debug endpoint to inspect the current rate-limit state
- Is fully configurable via environment variables
- Includes automated tests and CI using GitHub Actions

This is intentionally backend-focused. There is no application-specific business logic beyond rate limiting.

## High-level architecture

- FastAPI for request handling and dependency injection
- Startup lifecycle initialization for shared state (settings, store, rate limiter)
- Pluggable state backend (memory or file)
- Dependency-based enforcement of rate limits
- Configuration-driven behavior using environment variables
- Stateless container image, with persistence handled via Docker volumes when needed

## Running locally (without Docker)

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file (example):
  ```bash
  STATE__BACKEND=memory
  RATE_LIMIT__REQUESTS_PER_WINDOW=5
  RATE_LIMIT__WINDOW_SECONDS=60
  APP__NAME=Rate Limiter API
  ```
3. Start the server:
  ```bash
  uvicorn app.main:app --reload
  ```
4. Open Swagger UI:
  > [http://localhost:8000/docs](http://localhost:8000/docs)
Use the `X-API-Key` header when calling protected endpoints.


## Running with Docker

The Docker image is environment-agnostic. All configuration is injected at runtime.

### Build the image

```bash
docker build -t rate-limiter .
```

### Run the container

```bash
docker run \
  --env-file .env \
  -p 8000:8000 \
  rate-limiter
```

## Running with Docker Compose (recommended)

Docker Compose is the easiest way to run the service with optional persistent state.
```bash
docker compose up --build
```

### What Docker Compose provides:

- Loads environment variables from `.env`
- Exposes the API on port 8000
- Mounts a named volume for file-based persistence
- Allows container restarts without losing state

To stop the service:
```bash
docker compose down
```

## Configuration

All configuration is done via environment variables.

Examples:
```json
STATE__BACKEND=memory            # memory | file
STATE__FILE_PATH=/data/state.json
RATE_LIMIT__REQUESTS_PER_WINDOW=10
RATE_LIMIT__WINDOW_SECONDS=60
APP__NAME=Rate Limiter API
```

There are no hardcoded configuration values in the application.

## Testing

Run tests locally:
```bash
pytest -v
```

Tests use the in-memory backend and do not require Docker.

## CI (GitHub Actions)

The project includes a GitHub Actions workflow that:
- Sets up Python
- Installs dependencies
- Runs tests on every push and pull request
- Configuration in CI is injected using GitHub Secrets rather than .env files.

## Why this project exists

This project is meant to demonstrate:
- Clean FastAPI lifecycle management
- Dependency-driven request enforcement
- Safe handling of shared application state
- Environment-based configuration
- Docker-friendly service design
- Basic CI hygiene
It is intentionally small, readable, and focused on engineering fundamentals rather than features.
