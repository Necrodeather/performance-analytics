import uvicorn
from fastapi import FastAPI

from src.container import AppContainer
from src.performance_analytics.public.http.endpoints import analytic_router
from src.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG)
    app.container = AppContainer()
    app.include_router(analytic_router)

    return app


app = create_app()


def start():
    uvicorn.run(
        app=app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
    )


if __name__ == "__main__":
    start()
