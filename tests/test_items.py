import os, pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db import get_session

TEST_DB = "sqlite:///./test.db"

def setup_module():
    if os.path.exists("test.db"):
        os.remove("test.db")
    engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def _get_session():
        engine_local = create_engine(TEST_DB, connect_args={"check_same_thread": False})
        with Session(engine_local) as session:
            yield session
    app.dependency_overrides[get_session] = _get_session

@pytest.mark.asyncio
async def test_items_crud():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # list empty
            r = await ac.get("/v1/items"); assert r.status_code == 200 and r.json() == []
            # create
            r = await ac.post("/v1/items", json={"name":"widget","description":"first"}); assert r.status_code == 201
            iid = r.json()["id"]
            # update
            r = await ac.put(f"/v1/items/{iid}", json={"name":"widget2","description":"updated"}); assert r.status_code == 200
            # get
            r = await ac.get(f"/v1/items/{iid}"); assert r.status_code == 200 and r.json()["name"] == "widget2"
            # delete
            r = await ac.delete(f"/v1/items/{iid}"); assert r.status_code == 204
            # confirm 404
            r = await ac.get(f"/v1/items/{iid}"); assert r.status_code == 404
