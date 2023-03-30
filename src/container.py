from dependency_injector import containers, providers


from src.database import Database
from src.settings import settings
from src.performance_analytics.container import AnalyticContainer


class AppContainer(containers.DeclarativeContainer):

    resources = providers.Aggregate(
        sqlalchemy=providers.Singleton(Database, db_url=settings.DATABASE_URI),
    )

    performance_analytics = providers.Container(
        AnalyticContainer,
        session=resources.sqlalchemy.provided.session,
    )
