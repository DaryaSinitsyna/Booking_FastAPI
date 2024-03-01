from pydantic import BaseModel


class SHotelRooms(BaseModel):
    rooms_left: int
    room_id: int


class SHotelRoomsInfo(BaseModel):
    hotel_id: int
    rooms: list[SHotelRooms]
