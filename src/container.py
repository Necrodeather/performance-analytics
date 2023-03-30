from dependency_injector import containers, providers

from src.database import Database
from src.performance_analytics.container import AnalyticContainer
from src.settings import settings


class AppContainer(containers.DeclarativeContainer):

    resources = providers.Aggregate(
        sqlalchemy=providers.Singleton(
            Database,
            db_url=settings.DATABASE_URI,
            debug=settings.DEBUG,
        ),
    )

    performance_analytics = providers.Container(
        AnalyticContainer,
        session=resources.sqlalchemy.provided.session,
    )
