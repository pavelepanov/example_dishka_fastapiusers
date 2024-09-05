from dataclasses import dataclass, field

from fastapi import APIRouter, Depends

from src.example_dishka_fastapiusers.data_access.models.user import UserDb
from src.example_dishka_fastapiusers.dependencies.fastapi_users import current_user

private_router = APIRouter(prefix="/private", tags=["private"])


@dataclass(frozen=True)
class Private:
    status: str = field(default="It is private router")


@private_router.get("/", response_model=Private)
async def health_check(user: UserDb = Depends(current_user)) -> Private:
    return Private(status="It is private router")
