from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class ServiceModel(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    path: Mapped[list["PathModel"]] = relationship(
        "PathModel",
        back_populates="service",
        lazy="subquery",
    )


class PathModel(Base):
    __tablename__ = "paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path_url: Mapped[str] = mapped_column(String(255))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    service: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="path")
    statistic: Mapped[list["StatisticModel"]] = relationship(
        "StatisticModel",
        back_populates="path",
    )


class StatisticModel(Base):
    __tablename__ = "statistics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[int] = mapped_column(Integer)
    path_id: Mapped[int] = mapped_column(ForeignKey("paths.id"))
    path: Mapped["PathModel"] = relationship("PathModel", back_populates="statistic")
