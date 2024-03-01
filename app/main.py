from fastapi import FastAPI, Query, Depends
from datetime import date
from pydantic import BaseModel

from app.hotels.models import Hotels # noqa
from app.users.models import Users # noqa
from app.hotels.rooms.models import Rooms # noqa
from app.bookings.models import Bookings # noqa

from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.users.router import router_auth, router_users

app = FastAPI(
    title='Бронирование отелей'
)

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)
app.include_router(router_rooms)


