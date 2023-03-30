from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from src.performance_analytics.domain.schemas import ServiceCreate, ServiceStatistic

analytic_router = APIRouter()


@analytic_router.post(path='/metrics', status_code=status.HTTP_201_CREATED)
@inject
async def add_new_metrics(data: ServiceCreate, service=Depends(Provide['service'])) -> ServiceCreate:
    ...


@analytic_router.get(path='/metrics/<service-name: str>')
@inject
async def get_metrics(service_name: str, service=Depends(Provide['service'])) -> list[ServiceStatistic]:
    ...