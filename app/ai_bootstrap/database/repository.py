from typing import Generic, TypeVar

from sqlalchemy import desc
from sqlalchemy.orm import Session

T = TypeVar("T")


class GenericRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        return obj

    def get(self, id: str) -> T | None:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list[T]:
        return self.session.query(self.model).all()

    def update(self, obj: T) -> T:
        self.session.merge(obj)
        self.session.commit()
        return obj

    def delete(self, id: str) -> None:
        if obj := self.get(id):
            self.session.delete(obj)
            self.session.commit()

    def get_latest(self, n: int = 1) -> list[T]:
        return self.session.query(self.model).order_by(desc(self.model.id)).limit(n).all()

    def count(
        self,
    ) -> int:
        return self.session.query(self.model).count()

    def exists(self, **filters: object) -> bool:
        return self.session.query(self.model).filter_by(**filters).first() is not None
