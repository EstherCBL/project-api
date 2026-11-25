from pydantic import BaseModel, ConfigDict, Field

class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    capacity: int = Field(gt=0)
    location: str = Field(min_length=1)

class RoomUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    capacity: int = Field(gt=0)
    location: str = Field(min_length=1)

class RoomOut(BaseModel):
    id: int
    name: str
    capacity: int
    location: str

    model_config = ConfigDict(from_attributes=True)

class RoomPage(BaseModel):
    items: list[RoomOut]
    page: int
    size: int
    total: int

