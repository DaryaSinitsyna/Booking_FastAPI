from datetime import date
from typing import Optional

from sqlalchemy import select, or_, and_, func

from app.bookings.models import Bookings


from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(cls,
                                date_from: date,
                                date_to: date,
                                location: Optional[str] = None,
                                name: Optional[str] = None,
                                ):
        """
        WITH booked_rooms AS(
        SELECT *
        FROM bookings
        WHERE
        bookings.date_from between '2023-06-16' AND '2023-06-30'
        OR bookings.date_to between '2023-06-16' AND '2023-06-30'
        OR bookings.date_from < '2023-06-16' AND bookings.date_to > '2023-06-30'
        ),
        hotels_rooms_left AS (
            SELECT hotels.rooms_quantity - count(booked_rooms.room_id) AS rooms_left, rooms.hotel_id AS hotel_id
            FROM hotels
            LEFT OUTER JOIN rooms ON rooms.hotel_id = hotels.id
            LEFT OUTER JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            WHERE (hotels.location LIKE '%' || 'Алтай' || '%') AND (hotels.name LIKE '%' || 'Skala' || '%')
            GROUP BY hotels.rooms_quantity, rooms.hotel_id)
        SELECT * , hotels_rooms_left.rooms_left
        FROM hotels JOIN hotels_rooms_left ON hotels_rooms_left.hotel_id = hotels.id
        WHERE hotels_rooms_left.rooms_left > 0
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                    .where(
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

            hotels_rooms_left = (
                select(
                    (
                            Hotels.rooms_quantity - func.count(booked_rooms.c.room_id)
                    ).label("rooms_left"),
                    Rooms.hotel_id,
                )
                    .select_from(Hotels)
                    .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
                    .outerjoin(
                    booked_rooms,
                    booked_rooms.c.room_id == Rooms.id,
                )
                    .where(
                    (Hotels.location.contains(location.title()) if location else True),
                    (Hotels.name.contains(name.title()) if name else True)

                )
                    .group_by(Hotels.rooms_quantity, Rooms.hotel_id)
                    .cte("hotels_rooms_left")
            )

            get_hotels_info = (
                select(
                    Hotels.__table__.columns,
                    hotels_rooms_left.c.rooms_left,
                )
                    .select_from(Hotels)
                    .join(hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id)
                    .where(hotels_rooms_left.c.rooms_left > 0)
            )

            hotels_info = await session.execute(get_hotels_info)
            return hotels_info.mappings().all()

    @classmethod
    async def search_for_rooms(cls,
                               hotel_id: int,
                               date_from: date,
                               date_to: date,
                               ):
        """
        WITH booked_rooms AS(
        SELECT *
        FROM bookings
        WHERE
        bookings.date_from between '2023-06-16' AND '2023-06-30'
        OR bookings.date_to between '2023-06-16' AND '2023-06-30'
        OR bookings.date_from < '2023-06-16' AND bookings.date_to > '2023-06-30'
        )


        SELECT rooms.quantity - (COUNT(booked_rooms.room_id)FILTER (WHERE booked_rooms.room_id IS NOT NULL)) AS rooms_left,
        rooms.id AS id, rooms.name AS name, rooms.description AS description, rooms.price AS price,rooms.services AS services,
        rooms.quantity AS quantity, rooms.image_id AS image_id
        FROM rooms
        LEFT OUTER JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.hotel_id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id, rooms.id;
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                    .where(
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

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id).filter(
                        booked_rooms.c.room_id.is_not(None))).label(
                        "rooms_left"),
                    Rooms.id.label("id"),
                    Rooms.name.label("name"),
                    Rooms.description.label("description"),
                    Rooms.price.label("price"),
                    Rooms.services.label("services"),
                    Rooms.quantity.label("quantity"),
                    Rooms.image_id.label("image_id"),
                )
                    .select_from(Rooms)
                    .outerjoin(
                    booked_rooms,
                    booked_rooms.c.room_id == Rooms.id,
                )
                    .where(Rooms.hotel_id == hotel_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id, Rooms.id)
            )

            rooms_info = await session.execute(get_rooms_left)
            return {"hotel_id": hotel_id, "rooms": rooms_info.mappings().all()}
