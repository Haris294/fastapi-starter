import os
import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db import get_session
from app.models import Item

TEST_DB = "sqlite:///./test.db"

def setup_module():
    # fresh test db each run
    if os.path.exists("test.db"):
        os.remove("test.db")
    engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    # override FastAPI dependency to use test engine
    def _get_session():
        engine_local = create_engine(TEST_DB, connect_args={"check_same_thread": False})
        with Session(engine_local) as session:
            yield session
    app.dependency_overrides[get_session] = _get_session

@pytest.mark.asyncio
async def test_items_crud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # empty list
        r = await ac.get("/items")
        assert r.status_code == 200
        assert r.json() == []

        # create
        r = await ac.post("/items", json={"name": "widget", "description": "first one"})
        assert r.status_code == 201
        data = r.json()
        assert data["id"] >= 1 and data["name"] == "widget"

        # list has one
        r = await ac.get("/items")
        assert r.status_code == 200
        assert len(r.json()) == 1

        # fetch by id
        item_id = data["id"]
        r = await ac.get(f"/items/{item_id}")
        assert r.status_code == 200
        assert r.json()["name"] == "widget"
