from fastapi import APIRouter, Depends
import time

from api.dependencies import rate_limit_dependency
from core.models import ResourceResponse

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@router.get(
    "/resource",
    response_model=ResourceResponse,
)
async def protected_resource(
    _: None = Depends(rate_limit_dependency),
) -> ResourceResponse:
    return ResourceResponse(
        message="You have accessed a rate-limited resource",
        timestamp=time.time(),
    )
