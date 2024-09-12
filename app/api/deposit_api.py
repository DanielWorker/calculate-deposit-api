from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.bank_service.functions import BankFunctions
from app.bank_service.schemas import DepositSchema

router = APIRouter(prefix='/deposits')


@router.post('/calculate')
async def calculate_deposit_api(deposit: DepositSchema) -> Dict[str, float]:
    try:
        return BankFunctions.calculate_deposit(deposit)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
