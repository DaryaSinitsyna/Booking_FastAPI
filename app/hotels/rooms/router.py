from datetime import date

from fastapi import Query, APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SHotelRoomsInfo, SRoom
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_date(
        hotel_id: int,
        date_from: date = Query(date.today()),
        date_to: date = Query(date.today()),

) -> SHotelRoomsInfo:
    rooms = await HotelsDAO.search_for_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return rooms


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.get("/{room_id}")
async def get_room(
        room_id: int
) -> list[SRoom]:
    return await RoomDAO.find_all(id=room_id)
