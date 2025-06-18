from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseOrm
from .mixins import IntIdPkMixin


class UserOrm(BaseOrm, IntIdPkMixin):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
