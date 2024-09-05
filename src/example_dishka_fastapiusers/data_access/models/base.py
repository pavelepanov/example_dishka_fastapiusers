from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class BaseDb(AsyncAttrs, DeclarativeBase):
    """Base class for all database models."""
