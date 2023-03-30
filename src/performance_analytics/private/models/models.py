from datetime import time

from sqlalchemy import Integer, String, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class ServiceModel(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    service_name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(255))

    __mapper_args__ = {
        "polymorphic_identity": "service",
        "polymorphic_on": type,
    }


class ServiceStatisticModel(ServiceModel):
    __tablename__ = 'service_statistics'

    id: Mapped[int] = mapped_column(Integer, ForeignKey("service.id"), primary_key=True)
    response_time: Mapped[time] = mapped_column(Time)

    __mapper_args__ = {
        "polymorphic_load": "selectin",
        "polymorphic_identity": "manager",
    }
