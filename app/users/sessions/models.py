from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    access_token: Mapped[str]
    date_create: Mapped[datetime] = mapped_column(DateTime)
    expire: Mapped[datetime] = mapped_column(DateTime)

    def __str__(self):
        return f"Сессия {self.id}"
