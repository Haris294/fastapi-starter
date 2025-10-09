from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from .models import Item
from .db import get_session
from .schemas import ItemRead, ItemCreate

router = APIRouter()

@router.get("/items", response_model=list[ItemRead])
def list_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()

@router.post("/items", status_code=201, response_model=ItemRead)
def create_item(payload: ItemCreate, session: Session = Depends(get_session)):
    item = Item.model_validate(payload)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item

@router.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemCreate, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    item.name = payload.name
    item.description = payload.description
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(item)
    session.commit()
    return None
