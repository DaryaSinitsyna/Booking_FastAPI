from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.sessions.dao import SessionDAO


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_token, date_create, expire = create_access_token({"sub": str(user.id)})
            await SessionDAO.add(user_id=user.id,
                                 access_token=access_token,
                                 date_create=date_create,
                                 expire=expire)
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]|bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token)

        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if user.role != "admin":
            return RedirectResponse(request.url_for("admin:login"), status_code=403)

        return True


authentication_backend = AdminAuth(secret_key="...")