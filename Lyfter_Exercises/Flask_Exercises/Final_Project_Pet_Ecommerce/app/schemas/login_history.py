from pydantic import Field, IPvAnyAddress
from datetime import datetime

from app.schemas.read_schema import ReadSchema
from app.schemas.pagination import PaginationParams


class LoginHistoryRead(ReadSchema):
    id: int
    login_date: datetime
    user_id: int | None
    user_ip: IPvAnyAddress | None
    success: bool

class LoginHistoryListParams(PaginationParams):
    user_id: int | None = Field(default=None, ge=1)