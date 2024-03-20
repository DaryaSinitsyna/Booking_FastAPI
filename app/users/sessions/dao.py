from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import FailedToDeleteSession
from app.users.sessions.models import Session


class SessionDAO(BaseDAO):
    model = Session

    @classmethod
    async def delete_session(
            cls,
            user_id: int,
            access_token: str,
    ):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Session).filter(Session.access_token == access_token, Session.user_id == user_id))
            current_session = result.scalar_one_or_none()
            if current_session:
                await session.delete(current_session)
                await session.commit()
            else:
                raise FailedToDeleteSession
