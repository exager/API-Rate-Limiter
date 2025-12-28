import json
from typing import Optional
import aiofiles
import asyncio
from pathlib import Path

from core.models import RateLimitState
from stores.base import RateLimitStore


class FileRateLimitStore(RateLimitStore):
    def __init__(self, file_path: str) -> None:
        self._path = Path(file_path)
        self._lock = asyncio.Lock()

    async def _read_all(self) -> dict[str, dict]:
        if not self._path.exists():
            return {}
        async with aiofiles.open(self._path, "r") as f:
            content = await f.read()
            if not content:
                return {}
            return json.loads(content)

    async def _write_all(self, data: dict[str, dict]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(self._path, "w") as f:
            await f.write(json.dumps(data))

    async def get_state(self, api_key: str) -> Optional[RateLimitState]:
        async with self._lock:
            data = await self._read_all()
            raw = data.get(api_key)
            if raw is None:
                return None
            return RateLimitState(**raw)

    async def save_state(self, api_key: str, state: RateLimitState) -> None:
        async with self._lock:
            data = await self._read_all()
            data[api_key] = state.model_dump()
            await self._write_all(data)

    async def clear_state(self, api_key: str) -> None:
        async with self._lock:
            data = await self._read_all()
            data.pop(api_key, None)
            await self._write_all(data)
