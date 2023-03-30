from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional, TypeVar

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.performance_analytics.private.models import models

Model = TypeVar("Model")


class AnalyticRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session = session_factory

    async def get_service(self, service_name: str) -> Optional[models.ServiceModel]:
        stmt = select(models.ServiceModel).where(models.ServiceModel.name == service_name.lower())
        async with self.session() as session:
            result = await session.execute(stmt)

        return result.scalars().one_or_none()

    async def get_path(self, service_id: int, path: str) -> Optional[models.ServiceModel]:
        stmt = select(models.PathModel).where(
            models.PathModel.path_url == path,
            models.PathModel.service_id == service_id,
        )
        async with self.session() as session:
            result = await session.execute(stmt)

        return result.scalars().one_or_none()

    async def get_statistic_metric(self, method: str, path_id) -> int:
        FUNC_METHOD = {
            "MIN": func.min,
            "MAX": func.max,
            "AVG": func.min,
            "P99": func.percentile_cont,
        }
        if method == "P99":
            stmt = select(FUNC_METHOD[method](0.9).within_group(models.StatisticModel.time)).where(
                models.StatisticModel.path_id == path_id,
            )
        else:
            stmt = select(FUNC_METHOD[method](models.StatisticModel.time)).where(
                models.StatisticModel.path_id == path_id,
            )
        async with self.session() as session:
            result = await session.execute(stmt)

        return result.scalar_one()

    async def create_service(self, service_name: str) -> models.ServiceModel:
        return await self.__create(models.ServiceModel, name=service_name.lower())

    async def create_path(self, service_id: int, path: str) -> models.PathModel:
        return await self.__create(models.PathModel, service_id=service_id, path_url=path)

    async def create_response_statistic(
        self,
        path_id: int,
        response_time: int,
    ) -> models.StatisticModel:
        return await self.__create(models.StatisticModel, path_id=path_id, time=response_time)

    async def __create(self, model: Model, **kwargs) -> Model:
        stmt = insert(model).values(kwargs).returning(model)
        async with self.session() as session:
            result = await session.execute(stmt)
            await session.commit()

        return result.scalar_one()
