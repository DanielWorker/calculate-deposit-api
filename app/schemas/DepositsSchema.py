from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class DepositSchema(BaseModel):
    date: str
    periods: int = Field(ge=1, le=60)
    amount: float = Field(ge=10000, le=3000000)
    rate: float = Field(ge=1, le=8)

    @field_validator('date', mode='before')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%d.%m.%Y')
        except ValueError:
            raise ValueError("value is not a valid datetime (format '%d.%m.%Y' expected)")

        return v
