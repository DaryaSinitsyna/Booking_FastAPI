from fastapi import APIRouter, Depends, Security
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.models import Users
from datetime import date

from app.tasks.tasks import send_booking_confirmation_email
from fastapi import BackgroundTasks

from app.users.router import header

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user), header_value=Security(header)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


# @router.post('')
# async def add_bookings(
#         room_id: int,
#         date_from: date,
#         date_to: date,
#         user: Users = Depends(get_current_user)
# ) -> SBookingInfo:
#     return await BookingDAO.add(user.id, room_id, date_from, date_to)


@router.post("")
async def add_booking(
        background_tasks: BackgroundTasks,
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user),
        header_value=Security(header)
):
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    # вариант с использованием celery
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    # вариант с использованием background tasks
    background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict


@router.delete('', status_code=204)
async def remove_bookings(
        booking_id: int,
        current_user: Users = Depends(get_current_user),
        header_value=Security(header)
):
    await BookingDAO.delete_booking(booking_id, current_user.id)
