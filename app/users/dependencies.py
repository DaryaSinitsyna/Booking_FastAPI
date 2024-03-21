from fastapi import Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.exceptions import (
    TokenExpiredException,
    IncorrectTokenFormatException,
    UserIsNotPresentException,
    TokenAbsentException
)

# from app.users.dao import UsersDAO
from app.users.dao import UsersDAO
from app.users.sessions.dao import SessionDAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    user_id = 0
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
        user_id = int(payload.get("sub"))
    except ExpiredSignatureError:
        await SessionDAO.delete_session(user_id=user_id, access_token=token)
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    if not user_id:
        raise UserIsNotPresentException

    user_session = await SessionDAO.find_one_or_none(user_id=user_id, access_token=token)
    if not user_session:
        raise UserIsNotPresentException

    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserIsNotPresentException
    return user


# вариант получения токена из cookie
# def get_token(request: Request):
#     token = request.cookies.get("booking_access_token")
#     if not token:
#         raise TokenAbsentException
#     return token
#
#
# async def get_current_user(token: str = Depends(get_token)):
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, settings.ALGORITHM
#         )
#     except ExpiredSignatureError:
#         raise TokenExpiredException
#     except JWTError:
#         raise IncorrectTokenFormatException
#
#     user_id: str = payload.get("sub")
#     if not user_id:
#         raise UserIsNotPresentException
#     user = await UsersDAO.find_one_or_none(id=int(user_id))
#     if not user:
#         raise UserIsNotPresentException
#
#     return user
