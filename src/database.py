from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class Database:
    def __init__(self, db_url: str, debug: bool):
        self._engine = create_async_engine(url=db_url, echo=debug, future=debug)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                bind=self._engine,
                class_=AsyncSession,
            ),
        )

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
