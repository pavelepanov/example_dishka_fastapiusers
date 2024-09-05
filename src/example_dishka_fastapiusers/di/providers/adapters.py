from typing import AsyncIterable

from dishka import Provider, Scope, provide
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.example_dishka_fastapiusers.config import (
    DatabaseConfig,
    SecretJwtConfig,
    SecretManagerConfig,
)
from src.example_dishka_fastapiusers.data_access.models.user import UserDb
from src.example_dishka_fastapiusers.dependencies.fastapi_users import UserManager


class SqlalchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> DatabaseConfig:
        return DatabaseConfig.from_env()

    @provide(scope=Scope.APP)
    def provide_engine(self, config: DatabaseConfig) -> AsyncEngine:
        # PostgreSQL Максимум соединений по умолчанию - 100
        #  с данными настройками 4 воркера займут 40 соединений
        return create_async_engine(
            config.db_uri,
            pool_size=10,
            max_overflow=0,
            pool_pre_ping=True,
            connect_args={
                "timeout": 15,
                "command_timeout": 5,
                "server_settings": {
                    "jit": "off",
                    "application_name": "web-api",
                },
            },
        )

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session


class FastapiUsersProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_secret_jwt_config(self) -> SecretJwtConfig:
        return SecretJwtConfig.from_env()

    @provide(scope=Scope.APP)
    def provide_secret_manager_config(self) -> SecretManagerConfig:
        return SecretManagerConfig.from_env()

    @provide(scope=Scope.APP)
    def provide_jwt_strategy(self, secret_jwt: SecretJwtConfig) -> JWTStrategy:
        return JWTStrategy(secret=secret_jwt.secret_jwt, lifetime_seconds=3600)

    @provide(scope=Scope.APP)
    def provide_auth_backend(self, jwt_strategy: JWTStrategy) -> AuthenticationBackend:
        cookie_transport = CookieTransport(cookie_name="smartfit", cookie_max_age=3600)

        auth_backend = AuthenticationBackend(
            name="jwt",
            transport=cookie_transport,
            get_strategy=lambda: jwt_strategy,
        )

        return auth_backend

    @provide(scope=Scope.REQUEST)
    def provide_user_manager(
        self,
        secret_jwt: SecretJwtConfig,
        secret_manager: SecretManagerConfig,
        session: AsyncSession,
    ) -> UserManager:
        user_db = SQLAlchemyUserDatabase(session, UserDb)
        user_manager = UserManager(
            reset_password_token_secret=secret_jwt.secret_jwt,
            verification_token_secret=secret_manager.secret_manager,
            user_db=user_db,
        )
        return user_manager
