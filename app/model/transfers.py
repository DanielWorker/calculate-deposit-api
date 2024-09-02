import enum
from datetime import datetime

from sqlalchemy import ForeignKey, Float, Integer, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.model.database import Base, int_pk, str_null_true


class TransferStatus(enum.Enum):
    NEW = "new"
    LOCKED = "locked"
    DEPOSITED = "deposited"
    COMPLETED = "completed"
    FAILED = "failed"


class Transfer(Base):
    id: Mapped[int_pk]
    from_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[TransferStatus] = mapped_column(Enum(TransferStatus), nullable=False)
    error_message: Mapped[str_null_true]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"from_account_id={self.from_account_id!r}), "
                f"to_account_id={self.to_account_id!r}), "
                f"amount={self.amount!r}), "
                f"timestamp={self.timestamp!r}), "
                f"status={self.status!r}), "
                f"error_message={self.error_message!r}")

    def __repr__(self):
        return str(self)
