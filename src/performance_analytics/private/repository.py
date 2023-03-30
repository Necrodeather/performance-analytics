from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.performance_analytics.domain.schemas import ServiceCreate


class AnalyticRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session = session_factory

    async def add_new_metrics(self, data: ServiceCreate) -> ServiceCreate:
        ...
