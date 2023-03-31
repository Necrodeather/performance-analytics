from typing import Optional

from fastapi import HTTPException

from src.performance_analytics.domain.schemas import ServiceCreate, ServiceStatistic
from src.performance_analytics.private import repository
from src.performance_analytics.private.models import PathModel, ServiceModel


class AnalyticService:
    def __init__(self, repository: repository.AnalyticRepository):
        self.repository = repository

    async def add_metrics(self, data: ServiceCreate) -> ServiceCreate:
        service = await self.__check_or_create_service(data.service_name)
        path = await self.__check_or_create_path(service.id, data.path)
        await self.repository.create_response_statistic(path.id, data.response_time)

        return data

    async def __check_or_create_service(self, service_name: str) -> ServiceModel:
        result = await self.repository.get_service(service_name)

        if not result:
            result = await self.repository.create_service(service_name)

        return result

    async def __check_or_create_path(self, service_id: int, path: str) -> PathModel:
        result = await self.repository.get_path(service_id, path)

        if not result:
            result = await self.repository.create_path(service_id, path)

        return result

    async def get_metrics(self, service_name: str) -> list[Optional[ServiceStatistic]]:
        result = []
        data = await self.repository.get_service(service_name)

        if not data:
            raise HTTPException(status_code=404, detail="Service is not found")

        if not data.path:
            return []

        for path in data.path:
            path_result = await self.generate_metrics(path)
            result.append(path_result)

        return result

    async def generate_metrics(self, path: PathModel) -> ServiceStatistic:
        result = {
            "path": path.path_url,
            "average": await self.repository.get_statistic_metric("AVG", path.id),
            "min": await self.repository.get_statistic_metric("MIN", path.id),
            "max": await self.repository.get_statistic_metric("MAX", path.id),
            "p99": await self.repository.get_statistic_metric("P99", path.id),
        }
        return ServiceStatistic.parse_obj(result)
