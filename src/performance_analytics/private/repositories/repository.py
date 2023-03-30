from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.performance_analytics.private.models import PathModel, StatisticModel, ServiceModel
from src.performance_analytics.private.repositories.base import BaseRepository


class AnalyticRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session = session_factory
        self.base = BaseRepository(self.session)

    async def get_service(self, service_name: str) -> Optional[ServiceModel]:
        stmt = (
            select(ServiceModel)
            .where(
                ServiceModel.service_name == service_name.lower()
            )
        )
        async with self.session() as session:
            result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound:
            return

    async def get_path(self, service_id: int, path: str) -> Optional[ServiceModel]:
        stmt = select(PathModel).where(PathModel.path == path, PathModel.service_id == service_id)
        async with self.session() as session:
            result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound:
            return

    async def create_service(self, service_name: str) -> ServiceModel:
        return await self.base.create(ServiceModel, service_name=service_name.lower())

    async def create_path(self, service_id: int, path: str) -> PathModel:
        return await self.base.create(PathModel, service_id=service_id, path=path)

    async def create_response_statistic(self, path_id: int, response_time: int) -> StatisticModel:
        return await self.base.create(StatisticModel, path_id=path_id, response_time=response_time)

