from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SHotelRooms(BaseModel):
    rooms_left: int
    id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class SHotelRoomsInfo(BaseModel):
    hotel_id: int
    rooms: list[SHotelRooms]
