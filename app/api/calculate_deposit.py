from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta

from app.schemas.DepositsSchema import DepositSchema


def calculate_deposit(deposit: DepositSchema) -> Dict[str, float]:
    amount = deposit.amount
    start_date = datetime.strptime(deposit.date, '%d.%m.%Y')
    monthly_rate = deposit.rate / 12 / 100
    results = {}

    for i in range(deposit.periods):
        amount += amount * monthly_rate
        current_date = start_date + relativedelta(months=i)
        results[current_date.strftime('%d.%m.%Y')] = round(amount, 2)

    return results
