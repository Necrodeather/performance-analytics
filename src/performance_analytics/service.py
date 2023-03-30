from src.performance_analytics.domain.schemas import ServiceCreate
from src.performance_analytics.private.repository import AnalyticRepository


class AnalyticService:
    def __init__(self, repository: AnalyticRepository):
        self._repository = repository

    async def add_new_metrics(self, data: ServiceCreate) -> ServiceCreate:
        return await self._repository.add_new_metrics(data)
