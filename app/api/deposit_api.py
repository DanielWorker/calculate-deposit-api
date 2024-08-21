from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from .calculate_deposit import calculate_deposit
from ..schemas.DepositsSchema import DepositSchema

DepositApi = APIRouter(prefix='/deposits')


@DepositApi.post('/calculate')
def calculate_deposit_api(deposit: DepositSchema) -> Dict[str, float]:
    try:
        return calculate_deposit(deposit)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
