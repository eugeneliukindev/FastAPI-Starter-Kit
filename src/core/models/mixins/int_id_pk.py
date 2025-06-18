from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class IntUserIdMixin(IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
