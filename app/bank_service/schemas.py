from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DepositSchema(BaseModel):
    date: str
    periods: int = Field(..., ge=1, le=60)
    amount: float = Field(..., ge=10000, le=3000000)
    rate: float = Field(..., ge=1, le=8)

    @field_validator('date', mode='before')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Value is not a valid datetime (format '%d.%m.%Y' expected)")

        return v


class UserCreate(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    passport_num: str = Field(...)


class UserResponse(BaseModel):
    id: int = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    passport_num: str = Field(...)


class AccountType(str, Enum):
    CURRENT = "current"            # Текущий счет
    SAVINGS = "savings"            # Накопительный счет
    FOREIGN_CURRENCY = "foreign_currency"  # Валютный счет
    FIXED_DEPOSIT = "fixed_deposit"  # Депозитный счет
    INVESTMENT = "investment"      # Инвестиционный счет


class AccountCreate(BaseModel):
    user_id: int = Field(...)
    type: AccountType = Field(...)


class AccountResponse(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    type: AccountType = Field(...)
    balance: float = Field(...)
    locked_balance: float = Field(...)


class TransferStatus(str, Enum):
    NEW = "new"
    LOCKED = "locked"
    DEPOSITED = "deposited"
    COMPLETED = "completed"
    FAILED = "failed"


class TransferCreate(BaseModel):
    from_account_id: int = Field(...)
    to_account_id: int = Field(...)
    amount: float = Field(..., gt=0)


class TransferResponse(BaseModel):
    id: int = Field(...)
    from_account_id: int = Field(...)
    to_account_id: int = Field(...)
    amount: float = Field(...)
    timestamp: datetime = Field(...)
    status: TransferStatus = Field(...)
    error_message: Optional[str] = None


class DepositCreate(BaseModel):
    account_id: int = Field(...)
    amount: float = Field(..., gt=0)


class DepositResponse(BaseModel):
    id: int = Field(...)
    type: AccountType = Field(...)
    balance: float = Field(...)


class WithdrawCreate(BaseModel):
    account_id: int = Field(...)
    amount: float = Field(..., gt=0)


class WithdrawResponse(BaseModel):
    id: int = Field(...)
    type: AccountType = Field(...)
    balance: float = Field(...)
