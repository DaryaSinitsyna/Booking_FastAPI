from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingInfo
from app.users.dependencies import get_current_user
from app.users.models import Users
from datetime import date

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
async def add_bookings(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
) -> list[SBookingInfo]:
    return await BookingDAO.add(user.id, room_id, date_from, date_to)


@router.delete('', status_code=204)
async def remove_bookings(
        booking_id: int,
        current_user: Users = Depends(get_current_user)
):
    await BookingDAO.delete_booking(booking_id, current_user.id)


