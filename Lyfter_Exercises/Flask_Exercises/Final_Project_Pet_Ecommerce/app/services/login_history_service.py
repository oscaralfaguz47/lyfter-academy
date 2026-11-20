from collections.abc import Sequence

from app.repositories.login_history_repository import LoginHistoryRepository
from app.models.login_history import LoginHistory
from app.schemas.login_history import LoginHistoryListParams

class LoginHistoryService:
    def __init__(self, repository: LoginHistoryRepository) -> None:
        self._repository = repository

    def list_login_history(self, params: LoginHistoryListParams) -> tuple[Sequence[LoginHistory], int]:
        return self._repository.list(params), self._repository.count(params)