from collections.abc import Sequence
from typing import Any, cast

from sqlalchemy import ColumnElement, CursorResult, insert, select, text, update
from sqlalchemy.orm import Session

from backend.models.issues import Issue as IssueModel


class IssueRepository:
    def __init__(self, session: Session, filters: dict | None = None):
        self.session = session
        self.table = IssueModel
        self.filters: dict[str, Any] = {}
        self.where: list[ColumnElement[bool]] = []
        self.set_filters(filters or {})

    def set_filters(self, filters: dict[str, Any]) -> None:
        self.filters = filters
        self.where = self._create_filter(filters)

    def _create_filter(self, filters: dict[str, Any]) -> list[ColumnElement[bool]]:
        where: list[ColumnElement[bool]] = []
        for key, value in filters.items():
            if not value:
                continue

            attribute: ColumnElement[bool] = getattr(self.table, key)
            match key:
                case "title" | "description":
                    where.append(attribute.like(text(f"%{value}%")))
                case "status" | "priority":
                    where.append(attribute == str(value))
                case "active":
                    where.append(attribute.is_(True))
                case _:
                    where.append(attribute == value)

        return where

    def get_items(self) -> Sequence[IssueModel]:
        return self.session.execute(select(self.table).where(*self.where)).scalars().fetchall()

    def get_by_id(self, issue_id: int) -> IssueModel | None:
        statement = select(self.table).where(self.table.id == issue_id, self.table.active.is_(True))
        return self.session.execute(statement).scalar_one_or_none()

    def create(self, item: dict) -> int:
        """Insert new value and return primary key"""

        result = cast(CursorResult, self.session.execute(insert(self.table).values(item)))
        self.session.flush()

        # check that data was inserted
        if result.rowcount == 0 or result.inserted_primary_key is None:
            raise ValueError("Failed to save an item")

        return result.inserted_primary_key[0]

    def update(self, item: dict) -> int:
        if not self.where:
            raise ValueError("Missing query where statement")

        statement = update(self.table).values(item).where(*self.where)
        result = cast(CursorResult, self.session.execute(statement))

        # check that data was updated
        if result.rowcount == 0:
            raise ValueError("Failed to save an item")

        return self.filters["id"]
