import asyncio
from datetime import date
from typing import Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.hotels.rooms.schemas import SHotelRoomsInfo
from app.hotels.schemas import SHotelInfo, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{hotel_id}")
async def get_hotel(
        hotel_id: int
) -> list[SHotel]:
    return await HotelsDAO.find_all(id=hotel_id)


@router.get("")
@cache(expire=20)
async def get_hotels_by_location_name_date(
        location: Optional[str] = None,
        name: Optional[str] = None,
        date_from: date = Query(date.today()),
        date_to: date = Query(date.today()),

) -> list[SHotelInfo]:
    await asyncio.sleep(3)
    hotels = await HotelsDAO.search_for_hotels(date_from=date_from, date_to=date_to, location=location, name=name)
    return hotels

