from typing import final

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.config import settings
from app.utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    @final
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}>"
            f"({', '.join([f'{k}={v!r}' for k, v in self.__dict__.items() if k != '_sa_instance_state'])})"
        )

    __str__ = __repr__
