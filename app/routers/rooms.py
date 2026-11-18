from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import require_admin
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate, RoomOut, RoomPage

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("", response_model=RoomPage)
def list_rooms(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    total = db.query(Room).count()
    rooms = db.query(Room).offset(skip).limit(size).all()
    
    return {
        "items": rooms,
        "total": total,
        "page": page,
        "size": size
    }

@router.post("", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(
    room_in: RoomCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    db_room = Room(**room_in.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.put("/{room_id}", response_model=RoomOut)
def update_room(
    room_id: int,
    room_in: RoomUpdate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")
    
    update_data = room_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Sala não encontrada.")
    
    db.delete(db_room)
    db.commit()
    return None