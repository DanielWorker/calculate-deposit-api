import enum

from sqlalchemy import ForeignKey, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.model.database import Base, int_pk


class AccountType(str, enum.Enum):
    CURRENT = "current"            # Текущий счет
    SAVINGS = "savings"            # Накопительный счет
    FOREIGN_CURRENCY = "foreign_currency"  # Валютный счет
    FIXED_DEPOSIT = "fixed_deposit"  # Депозитный (срочный) счет
    INVESTMENT = "investment"      # Инвестиционный счет


class Account(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    locked_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"user_id={self.user_id!r}), "
                f"type={self.type!r}), "
                f"balance={self.balance!r}), "
                f"locked_balance={self.locked_balance!r}")

    def __repr__(self):
        return str(self)
