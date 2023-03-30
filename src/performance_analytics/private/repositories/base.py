from contextlib import AbstractAsyncContextManager
from typing import TypeVar, Callable

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session = session_factory

    async def create(self, model: Model, **kwargs) -> Model:
        stmt = insert(model).values(kwargs).returning(model)
        async with self.session() as session:
            result = await session.execute(stmt)
            await session.commit()

        return result.scalar_one()
