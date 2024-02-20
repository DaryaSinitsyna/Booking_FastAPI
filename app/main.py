from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel

from app.hotels.models import Hotels # noqa
from app.users.models import Users # noqa
from app.hotels.rooms.models import Rooms # noqa
from app.bookings.models import Bookings # noqa

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


class HotelSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: bool = None,
            stars: int = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


@app.get("/hotels")
def get_hotels(
        search_args: HotelSearchArgs = Depends()
):

    return search_args


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/booking")
def add_booking(booking: SBooking):
    pass
