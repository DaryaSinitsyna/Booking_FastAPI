from fastapi import APIRouter, Request, Response, Depends, Cookie, Security
from fastapi.security import APIKeyHeader

from app.exceptions import UserAlreadyExistsException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.sessions.dao import SessionDAO

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Users"],
)

header = APIKeyHeader(name="Authorization")


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token, date_create, expire = create_access_token({"sub": str(user.id)})
    await SessionDAO.add(user_id=user.id,
                         access_token=access_token,
                         date_create=date_create,
                         expire=expire)
    response.headers["Authorization"] = access_token
    return {"Authorization": access_token}


# @router_auth.post("/login")
# async def login_user(response: Response, user_data: SUserAuth):
#     user = await authenticate_user(user_data.email, user_data.password)
#     access_token = create_access_token({"sub": str(user.id)})
#     response.set_cookie("booking_access_token", access_token)
#     return {"booking_access_token": access_token}

@router_auth.post("/logout")
async def logout_user(request: Request, current_user: Users = Depends(get_current_user), header_value=Security(header)):
    access_token = request.headers["Authorization"]
    await SessionDAO.delete_session(current_user.id, access_token)


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user), header_value=Security(header)):
    return current_user
