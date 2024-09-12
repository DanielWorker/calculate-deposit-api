from sqlalchemy import ForeignKey, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.bank_service.schemas import AccountType
from app.database import Base, int_pk


class Account(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    locked_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"user_id={self.user_id!r}, "
                f"type={self.type!r}, "
                f"balance={self.balance!r}, "
                f"locked_balance={self.locked_balance!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type.name,
            "balance": self.balance,
            "locked_balance": self.locked_balance
        }

    def to_basic_dict(self):
        return {
            "id": self.id,
            "type": self.type.name,
            "balance": self.balance
        }
