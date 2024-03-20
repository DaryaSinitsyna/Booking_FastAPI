from datetime import date

from pydantic import BaseModel


class SSession(BaseModel):
    id: int
    user_id: int
    access_token: str
    date_create: date
    date_end: date