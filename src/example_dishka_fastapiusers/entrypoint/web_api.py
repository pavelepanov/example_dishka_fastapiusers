from dishka.integrations.fastapi import FromDishka, setup_dishka
from fastapi import FastAPI

from src.example_dishka_fastapiusers.dependencies.fastapi_users import (
    auth_backend,
    fastapi_users,
)
from src.example_dishka_fastapiusers.di.main import container_factory
from src.example_dishka_fastapiusers.presentation.web_api.routers.private import (
    private_router,
)
from src.example_dishka_fastapiusers.presentation.web_api.routers.public import (
    public_router,
)
from src.example_dishka_fastapiusers.presentation.web_api.schemas.fastapi_users import (
    UserCreate,
    UserRead,
)


def init_di(app: FastAPI) -> None:
    setup_dishka(container_factory(), app)


def init_routers(app: FastAPI) -> None:

    app.include_router(
        fastapi_users.get_auth_router(FromDishka[auth_backend]),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(private_router)
    app.include_router(public_router)


def create_app() -> FastAPI:
    app = FastAPI()

    init_di(app)
    init_routers(app)

    return app
