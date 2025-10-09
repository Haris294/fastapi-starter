import pytest
from fastapi import APIRouter, Depends
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from fastapi_limiter.depends import RateLimiter
from app.main import app

# test-only route
rt = APIRouter(prefix="/v1")
@rt.get("/_rl_test", dependencies=[Depends(RateLimiter(times=3, seconds=5))])
def _rl_test():
    return {"ok": True}
app.include_router(rt)

@pytest.mark.asyncio
async def test_rate_limit():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            for _ in range(3):
                assert (await ac.get("/v1/_rl_test")).status_code == 200
            r = await ac.get("/v1/_rl_test")
            assert r.status_code == 429
