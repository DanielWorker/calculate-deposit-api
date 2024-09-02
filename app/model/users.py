from sqlalchemy.orm import Mapped

from app.model.database import Base, str_uniq, int_pk, str_null_false


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str_null_false]
    last_name: Mapped[str_null_false]
    passport_num:  Mapped[str_uniq]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r}), "
                f"last_name={self.last_name!r}), "
                f"passport_num={self.passport_num!r}")

    def __repr__(self):
        return str(self)
