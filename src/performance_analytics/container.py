from dependency_injector import containers, providers

from src.performance_analytics.private.repositories import AnalyticRepository
from src.performance_analytics.service import AnalyticService


class AnalyticContainer(containers.DeclarativeContainer):
    session = providers.Dependency()

    wiring_config = containers.WiringConfiguration(
        modules=['.public.http.endpoints'],
    )

    repository = providers.Factory(
        AnalyticRepository,
        session_factory=session,
    )

    service = providers.Factory(
        AnalyticService,
        repository=repository,
    )
