from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import RoomFullyBooked, FailedToDeleteEntry
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH booked_rooms AS(
        SELECT *
        FROM bookings
        WHERE room_id = 1 AND (
        bookings.date_from between '2023-06-16' AND '2023-06-30'
        OR bookings.date_to between '2023-06-16' AND '2023-06-30'
        OR bookings.date_from < '2023-06-16' AND bookings.date_to > '2023-06-30')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                        .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                Bookings.date_from.between(date_from, date_to),
                                Bookings.date_to.between(date_from, date_to),
                                and_(
                                    Bookings.date_from < date_from,
                                    Bookings.date_to > date_to,
                                )
                            )
                        )
                    ).cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id).filter(
                            booked_rooms.c.room_id.is_not(None))).label(
                            "rooms_left"
                        )
                    )
                        .select_from(Rooms)
                        .outerjoin(booked_rooms, booked_rooms.c.room_id == Rooms.id)
                        .where(Rooms.id == room_id)
                        .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # Для вывода SQL запрос в консоль
                # get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True})

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                            .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                            .returning(
                            Bookings.id,
                            Bookings.user_id,
                            Bookings.room_id,
                            Bookings.date_from,
                            Bookings.date_to,
                        )
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.mappings().one()
                else:
                    raise RoomFullyBooked
        except RoomFullyBooked:
            raise RoomFullyBooked
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"

    @classmethod
    async def delete_booking(
            cls,
            booking_id: int,
            current_user: int
    ):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Bookings).filter(Bookings.id == booking_id, Bookings.user_id == current_user))
            booking = result.scalar_one_or_none()
            if booking:
                await session.delete(booking)
                await session.commit()
            else:
                raise FailedToDeleteEntry
