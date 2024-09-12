from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.bank_service.functions import BankFunctions
from app.bank_service.schemas import UserCreate, UserResponse, AccountCreate, AccountResponse, TransferResponse, \
    TransferCreate, \
    DepositCreate, WithdrawCreate, DepositResponse, WithdrawResponse
from app.database import get_db

router = APIRouter(prefix='/users')


@router.get('/all', response_model=List[UserResponse])
async def find_all_users_api():
    try:
        return await BankFunctions.find_all_users()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/create', response_model=UserResponse)
async def create_user_api(user: UserCreate):
    try:
        return await BankFunctions.create_user(user)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/accounts/info')
async def user_accounts_info_api(user_id: int):
    try:
        return await BankFunctions.find_accounts(user_id=user_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/accounts/create', response_model=AccountResponse)
async def create_account_api(account: AccountCreate):
    try:
        return await BankFunctions.create_account(account)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/accounts/deposit', response_model=DepositResponse)
async def deposit_funds_api(deposit: DepositCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await BankFunctions.deposit_funds(deposit.account_id, deposit.amount, session)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/accounts/withdraw', response_model=WithdrawResponse)
async def withdraw_funds_api(withdraw: WithdrawCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await BankFunctions.withdraw_funds(withdraw.account_id, withdraw.amount, session)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/transfers/create', response_model=TransferResponse)
async def create_transfer_api(transfer: TransferCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await BankFunctions.transfer_funds(transfer, session)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
