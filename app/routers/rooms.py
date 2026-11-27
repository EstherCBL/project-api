from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.database import get_db
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomOut, RoomPage, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Rooms"])


def buscar_sala(db: Session, room_id: int) -> Room:
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(404, "Sala não encontrada.")
    return room


@router.get("", response_model=RoomPage)
def list_rooms(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    total = db.query(Room).count()
    rooms = db.query(Room).offset((page - 1) * size).limit(size).all()
    return {"items": rooms, "total": total, "page": page, "size": size}


@router.post("", response_model=RoomOut, status_code=201, dependencies=[Depends(require_admin)])
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    room = Room(**room_in.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.put("/{room_id}", response_model=RoomOut, dependencies=[Depends(require_admin)])
def update_room(room_id: int, room_in: RoomUpdate, db: Session = Depends(get_db)):
    room = buscar_sala(db, room_id)
    for campo, valor in room_in.model_dump().items():
        setattr(room, campo, valor)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db.delete(buscar_sala(db, room_id))
    db.commit()
