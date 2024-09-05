from dataclasses import dataclass, field

from fastapi import APIRouter

public_router = APIRouter(prefix="/public", tags=["public"])


@dataclass(frozen=True)
class Public:
    status: str = field(default="It is public router")


@public_router.get("/", response_model=Public)
async def health_check() -> Public:
    return Public(status="It is public router")
