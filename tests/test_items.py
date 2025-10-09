import os, pytest
from httpx import AsyncClient
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
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/items"); assert r.status_code == 200 and r.json() == []
        r = await ac.post("/items", json={"name":"widget","description":"first"}); assert r.status_code == 201
        iid = r.json()["id"]
        r = await ac.put(f"/items/{iid}", json={"name":"widget2","description":"updated"}); assert r.status_code == 200
        r = await ac.get(f"/items/{iid}"); assert r.status_code == 200 and r.json()["name"] == "widget2"
        r = await ac.delete(f"/items/{iid}"); assert r.status_code == 204
        r = await ac.get(f"/items/{iid}"); assert r.status_code == 404
