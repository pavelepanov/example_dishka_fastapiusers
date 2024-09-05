from dishka import AsyncContainer, make_async_container

from src.example_dishka_fastapiusers.di.providers.adapters import (
    FastapiUsersProvider,
    SqlalchemyProvider,
)


def container_factory() -> AsyncContainer:
    return make_async_container(SqlalchemyProvider(), FastapiUsersProvider())
