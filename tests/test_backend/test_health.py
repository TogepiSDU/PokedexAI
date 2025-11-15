import asyncio
import importlib.util
import sys
import os
import httpx


def load_app():
    sys.path.insert(0, os.path.abspath("backend"))
    spec = importlib.util.spec_from_file_location("main", "backend/main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


async def async_health_check():
    app = load_app()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "healthy"
        assert isinstance(data["timestamp"], str) and len(data["timestamp"]) > 0


def test_health_endpoint():
    asyncio.run(async_health_check())