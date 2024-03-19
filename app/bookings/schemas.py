from datetime import date

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SNewBooking(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date