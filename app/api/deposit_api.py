from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.api.calculate_deposit import calculate_deposit
from app.schemas.DepositsSchema import DepositSchema

DepositApi = APIRouter(prefix='/deposits')


@DepositApi.post('/calculate')
def calculate_deposit_api(deposit: DepositSchema) -> Dict[str, float]:
    try:
        return calculate_deposit(deposit)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
