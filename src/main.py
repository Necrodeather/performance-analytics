import uvicorn
from fastapi import FastAPI

from src.container import AppContainer
from src.settings import settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.container = AppContainer()

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
    )
