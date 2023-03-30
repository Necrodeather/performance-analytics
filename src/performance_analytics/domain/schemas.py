from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator


class AbstractModel(BaseModel):
    class Config:
        orm_mode = True


class Service(AbstractModel):
    path: str

    @validator("path", pre=True)
    def validate_path(cls, value: str) -> str:
        if "/" != value[0]:
            raise ValueError("This path is specified incorrectly")
        return value


class ServiceCreate(Service):
    service_name: str = Field(alias="serviceName")
    response_time: PositiveInt = Field(alias="responseTimeMs")


class ServiceStatistic(Service):
    average: PositiveInt
    min_time: PositiveInt = Field(alias="min")
    max_time: PositiveInt = Field(alias="max")
    p99: Optional[PositiveInt]
