from typing import Optional

from pydantic import BaseModel, FileUrl, Field, PositiveInt


class AbstractModel(BaseModel):
    class Config:
        orm_mode = True


class Service(AbstractModel):
    path: FileUrl


class ServiceCreate(Service):
    service_name = Field(alias='serviceName')
    response_time = Field(alias='responseTimeMs')


class ServiceStatistic(Service):
    average: PositiveInt
    min: PositiveInt
    max: PositiveInt
    p99: Optional[PositiveInt]
