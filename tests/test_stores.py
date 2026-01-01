import pytest
import asyncio
import os
from pathlib import Path

from core.models import RateLimitState
from stores.memory_store import InMemoryRateLimitStore
from stores.file_store import FileRateLimitStore


def test_memory_store_basic_operations():
    store = InMemoryRateLimitStore()
    state = RateLimitState(count=1)

    store.save_state("key1", state)
    loaded = store.get_state("key1")

    assert loaded is not None
    assert loaded.count == 1

    store.clear_state("key1")
    assert store.get_state("key1") is None


@pytest.mark.asyncio
async def test_file_store_persistence(tmp_path: Path):
    file_path = tmp_path / "rate_limits.json"
    store = FileRateLimitStore(str(file_path))

    state = RateLimitState(count=2)

    await store.save_state("key1", state)
    loaded = await store.get_state("key1")

    assert loaded is not None
    assert loaded.count == 2

    await store.clear_state("key1")
    cleared = await store.get_state("key1")

    assert cleared is None
