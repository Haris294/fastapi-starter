from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from .models import Item
from .db import get_session

router = APIRouter()

@router.get("/items")
def list_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()

@router.post("/items", status_code=201)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/items/{item_id}")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
