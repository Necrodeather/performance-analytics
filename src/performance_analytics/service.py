from fastapi import HTTPException

from src.performance_analytics.domain.schemas import ServiceCreate, ServiceStatistic
from src.performance_analytics.private.models import ServiceModel, PathModel
from src.performance_analytics.private.repositories import AnalyticRepository
from src.performance_analytics.utils import generate_path


class AnalyticService:
    def __init__(self, repository: AnalyticRepository):
        self._repository = repository

    async def add_metrics(self, data: ServiceCreate) -> ServiceCreate:
        service = await self.__check_or_create_service(data.service_name)
        path = await self.__check_or_create_path(service.id, data.path)
        await self._repository.create_response_statistic(path.id, data.response_time)

        return data

    async def __check_or_create_service(self, service_name: str) -> ServiceModel:
        result = await self._repository.get_service(service_name)

        if not result:
            result = await self._repository.create_service(service_name)

        return result

    async def __check_or_create_path(self, service_id: int, path: str) -> PathModel:
        result = await self._repository.get_path(service_id, path)

        if not result:
            result = await self._repository.create_path(service_id, path)

        return result

    async def get_metrics(self, service_name: str) -> list[ServiceStatistic]:
        result = []
        data = await self._repository.get_service(service_name)

        if not data:
            raise HTTPException(status_code=404, detail='Service is not found')

        for path in data.path:
            path_result = await generate_path(path)
            result.append(path_result)

        return result


