from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from ..schemas.DepositsSchema import DepositSchema

DepositApi = APIRouter(prefix='/deposits')


@DepositApi.post('/calculate')
def calculate_deposit(deposit: DepositSchema) -> Dict[str, float]:
    try:
        amount = deposit.amount
        start_date = datetime.strptime(deposit.date, '%d.%m.%Y')
        monthly_rate = deposit.rate / 12 / 100
        results = {}

        for i in range(deposit.periods):
            amount += amount * monthly_rate
            current_date = start_date + relativedelta(months=i)
            results[current_date.strftime('%d.%m.%Y')] = round(amount, 2)

        return results

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
