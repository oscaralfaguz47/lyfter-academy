from sqlalchemy import Select, select, func
from sqlalchemy.orm import Session
from collections.abc import Sequence

from app.models.login_history import LoginHistory
from app.schemas.login_history import LoginHistoryListParams

class LoginHistoryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entry: LoginHistory) -> LoginHistory:
        self._session.add(entry)
        self._session.flush()
        return entry

    def list(self, params: LoginHistoryListParams) -> Sequence[LoginHistory]:
        query = self._filtered(params).order_by(LoginHistory.id.desc()).offset(params.offset).limit(params.per_page)
        return self._session.scalars(query).all()

    def count(self, params: LoginHistoryListParams) -> int:
        query = self._filtered(params).with_only_columns(func.count(LoginHistory.id))
        return self._session.scalar(query) or 0



    def _filtered(self, params: LoginHistoryListParams) -> Select:
        query = select(LoginHistory)
        if params.user_id is not None:
            query = query.where(LoginHistory.user_id == params.user_id)
        return query

