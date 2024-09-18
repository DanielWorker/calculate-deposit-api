from sqlalchemy import select

from app.database import async_session_maker

# TODO: move into bank_service/dao.py
class BaseDAO:
    @classmethod
    async def find_all(cls, model, **filter_by):
        async with async_session_maker() as session:
            query = select(model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
