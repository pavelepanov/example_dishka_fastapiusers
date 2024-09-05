from typing import Optional

from dishka.integrations.fastapi import FromDishka, inject
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelperProtocol

from src.example_dishka_fastapiusers.data_access.models.user import UserDb


class UserManager(IntegerIDMixin, BaseUserManager[UserDb, int]):
    def __init__(
        self,
        reset_password_token_secret: str,
        verification_token_secret: str,
        user_db: BaseUserDatabase[models.UP, models.ID],
        password_helper: Optional[PasswordHelperProtocol] = None,
    ):
        self.reset_password_token_secret = reset_password_token_secret
        self.verification_token_secret = verification_token_secret
        super().__init__(user_db, password_helper)


@inject
async def get_user_manager(user_manager: FromDishka[UserManager]):
    return user_manager


@inject
async def get_jwt_strategy(jwt_strategy: FromDishka[JWTStrategy]):
    return jwt_strategy


cookie_transport = CookieTransport(cookie_name="smartfit", cookie_max_age=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[UserDb, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
