from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from sqlalchemy import or_
from .models import Item
from .db import get_session
from .schemas import ItemRead, ItemCreate

router = APIRouter(prefix="/v1", tags=["items"])

@router.get("/items", response_model=list[ItemRead])
def list_items(
    q: str | None = Query(None, description="Search in name/description"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    stmt = select(Item)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Item.name.ilike(like), Item.description.ilike(like)))
    stmt = stmt.offset(offset).limit(limit)
    return session.exec(stmt).all()

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
