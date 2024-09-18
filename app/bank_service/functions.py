from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.bank_service.dao import BankDAO
from app.bank_service.schemas import DepositSchema, UserCreate, AccountCreate, TransferCreate


class BankFunctions:
    # TODO: don't use static methods

    @staticmethod
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

    @staticmethod
    async def create_user(user: UserCreate):
        try:
            return await BankDAO.create_user(user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Account with this passport number already exists")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create user. Error: {e}")

    @staticmethod
    async def find_all_users():
        users = await BankDAO.find_users()
        return [user.to_dict() for user in users]

    @staticmethod
    async def create_account(account: AccountCreate):
        try:
            return await BankDAO.create_account(account)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create account. Error: {e}")

    @staticmethod
    async def find_accounts(**filtered_by):
        accounts = await BankDAO.find_accounts(**filtered_by)
        return [account.to_basic_dict() for account in accounts]

    @staticmethod
    async def deposit_funds(account_id: int, amount: float, session: AsyncSession):
        async with session.begin():
            account = await BankDAO.find_account(account_id)
            if account is None:
                raise HTTPException(status_code=404, detail="Account not found")

            await BankDAO.update_account_balance(account, session, deposit=amount)
            await session.commit()

            return account

    @staticmethod
    async def withdraw_funds(account_id: int, amount: float, session: AsyncSession):
        async with session.begin():
            account = await BankDAO.find_account(account_id)
            if account is None:
                raise HTTPException(status_code=404, detail="Account not found")

            await BankDAO.update_account_balance(account, session, withdraw=amount)
            await session.commit()

            return account

    @staticmethod
    async def transfer_funds(transfer_data: TransferCreate, session: AsyncSession):
        from_account = await BankDAO.find_account(transfer_data.from_account_id)
        to_account = await BankDAO.find_account(transfer_data.to_account_id)

        if from_account is None:
            raise HTTPException(status_code=404, detail="From account not found")

        if to_account is None:
            raise HTTPException(status_code=404, detail="To account not found")

        transfer = await BankDAO.create_transfer(transfer_data)

        try:
            if from_account.balance - from_account.locked_balance < transfer_data.amount:
                error_message = f'Error at status: "{transfer.status}". Not enough funds for transfer'
                transfer.status = 'failed'
                transfer.error_message = error_message
                await BankDAO.update_transfer(transfer, session)
                await session.commit()
                return transfer

            async with session.begin():
                # from_account.locked_balance += transfer_data.amount
                # await BankDAO.update_account(from_account, session)
                await BankDAO.update_account_balance(from_account, session, lock=transfer_data.amount)
                transfer.status = 'locked'
                await BankDAO.update_transfer(transfer, session)

                # to_account.balance += transfer_data.amount
                # await BankDAO.update_account(to_account, session)
                await BankDAO.update_account_balance(to_account, session, deposit=transfer_data.amount)
                transfer.status = 'deposited'
                await BankDAO.update_transfer(transfer, session)

                # from_account.locked_balance -= transfer_data.amount
                # from_account.balance -= transfer_data.amount
                # await BankDAO.update_account(from_account, session)
                await BankDAO.update_account_balance(from_account, session, unlock=transfer_data.amount, withdraw=transfer_data.amount)
                transfer.status = 'completed'
                await BankDAO.update_transfer(transfer, session)

                await session.commit()

        except Exception as e:
            error_message = f'Error at status: "{transfer.status}". Details: {str(e)}'
            transfer.error_message = error_message
            transfer.status = 'failed'
            await BankDAO.update_transfer(transfer, session)
            await session.commit()
            return transfer

        return transfer
