from sqlalchemy.orm import Session

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    