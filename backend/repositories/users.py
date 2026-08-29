from typing import Any, cast

from sqlalchemy import CursorResult, select, update
from sqlalchemy.orm import Session

from backend.models.users import User as UserModel


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        self.table = UserModel

    def get_by_id(self, user_id: int) -> UserModel | None:
        statement = select(self.table).where(self.table.id == user_id, self.table.active.is_(True))
        return self.session.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> UserModel | None:
        statement = select(self.table).where(self.table.email == email, self.table.active.is_(True))
        return self.session.execute(statement).scalar_one_or_none()

    def create(self, user: UserModel) -> int:
        self.session.add(user)
        self.session.flush()

        return user.id

    def update(self, user_id: int, item: dict[str, Any]) -> int:
        statement = update(self.table).values(item).where(self.table.id == user_id)
        result = cast(CursorResult, self.session.execute(statement))

        if result.rowcount == 0:
            raise ValueError("Failed to save an item")

        return user_id
