from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bank_service.schemas import UserCreate, AccountCreate, TransferCreate
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.model.accounts import Account
from app.model.transfers import Transfer
from app.model.users import User


class BankDAO(BaseDAO):

    @staticmethod
    async def create_user(user: UserCreate) -> User:
        async with async_session_maker() as session:
            new_user = User(first_name=user.first_name, last_name=user.last_name, passport_num=user.passport_num)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    @staticmethod
    async def find_users(**filter_by) -> List[User]:
        async with async_session_maker() as session:
            query = select(User).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def create_account(account: AccountCreate) -> Account:
        async with async_session_maker() as session:
            new_account = Account(user_id=account.user_id, type=account.type)
            session.add(new_account)
            await session.commit()
            await session.refresh(new_account)
            return new_account

    @staticmethod
    async def find_account(account_id: int) -> Account:
        async with async_session_maker() as session:
            query = select(Account).filter_by(id=account_id)
            result = await session.execute(query)
            return result.scalars().first()

    @staticmethod
    async def find_accounts(user_id: int) -> List[Account]:
        async with async_session_maker() as session:
            query = select(Account).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def update_account(account: Account, session: AsyncSession) -> None:
        try:
            session.add(account)
            await session.flush()
        except Exception as e:
            raise Exception(f"Failed to update account {account.id}: {str(e)}")

    @staticmethod
    async def create_transfer(transfer: TransferCreate) -> Transfer:
        async with async_session_maker() as session:
            new_transfer = Transfer(from_account_id=transfer.from_account_id, to_account_id=transfer.to_account_id, amount=transfer.amount)
            session.add(new_transfer)
            await session.commit()
            await session.refresh(new_transfer)
            return new_transfer

    @staticmethod
    async def update_transfer(transfer: Transfer, session: AsyncSession) -> None:
        try:
            session.add(transfer)
            await session.flush()
        except Exception as e:
            raise Exception(f"Failed to update transfer {transfer.id}: {str(e)}")

    @staticmethod
    async def update_account_balance(
            account: Account,
            session: AsyncSession,
            *,
            deposit: float = 0.0,
            withdraw: float = 0.0,
            lock: float = 0.0,
            unlock: float = 0.0
    ) -> None:
        new_balance = account.balance + deposit - withdraw
        new_locked_balance = account.locked_balance + lock - unlock

        if new_balance < 0:
            raise HTTPException(status_code=400, detail="Balance cannot be negative")
        if new_locked_balance < 0:
            raise HTTPException(status_code=400, detail="Locked balance cannot be negative")

        account.balance = new_balance
        account.locked_balance = new_locked_balance

        session.add(account)
        await session.flush()
