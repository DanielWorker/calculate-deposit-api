from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from ..schemas.DepositsSchema import DepositSchema

DepositRoter = APIRouter(prefix='/deposits')


@DepositRoter.post('/calculate')
def calculate_deposit(deposit: DepositSchema) -> Dict[str, float]:
    try:
        amount = deposit.amount
        current_date = datetime.strptime(deposit.date, '%d.%m.%Y')
        monthly_rate = deposit.rate / 12 / 100
        results = {}

        for _ in range(deposit.periods):
            amount += amount * monthly_rate
            results[current_date.strftime('%d.%m.%Y')] = round(amount, 2)
            current_date += relativedelta(months=1)

        return results

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
