from dependency_injector.wiring import Provide, inject
from starlette import status

from src.performance_analytics.domain.schemas import ServiceCreate, ServiceStatistic

from fastapi import APIRouter, Depends

analytic_router = APIRouter(tags=["Performance Analytics"])


@analytic_router.post(path="/metrics", status_code=status.HTTP_201_CREATED)
@inject
async def add_new_metrics(
    data: ServiceCreate,
    service=Depends(Provide["service"]),
) -> ServiceCreate:
    return await service.add_metrics(data)


@analytic_router.get(path="/metrics/{service_name}")
@inject
async def get_metrics(
    service_name: str,
    service=Depends(Provide["service"]),
) -> list[ServiceStatistic]:
    return await service.get_metrics(service_name)
