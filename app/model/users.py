from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, str_uniq, int_pk, str_null_false


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    passport_num:  Mapped[str] = mapped_column(String, unique=True, nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r}, "
                f"last_name={self.last_name!r}, "
                f"passport_num={self.passport_num!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "passport_num": self.passport_num
        }
