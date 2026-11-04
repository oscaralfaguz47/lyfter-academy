from pydantic import BaseModel, ConfigDict, Field

MAX_PER_PAGE = 100


class PaginationParams(BaseModel):
    model_config = ConfigDict(extra="ignore")

    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=MAX_PER_PAGE)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page