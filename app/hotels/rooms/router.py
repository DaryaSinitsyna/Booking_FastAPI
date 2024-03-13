from datetime import date

from fastapi import Query

from app.hotels.dao import HotelsDAO
from app.hotels.rooms.schemas import SHotelRoomsInfo
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_date(
        hotel_id: int,
        date_from: date = Query(date.today()),
        date_to: date = Query(date.today()),

) -> SHotelRoomsInfo:
    rooms = await HotelsDAO.search_for_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return rooms
