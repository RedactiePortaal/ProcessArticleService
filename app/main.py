from dependency_injector.wiring import Provide
from fastapi import FastAPI, Depends

from app.containers import Container
from app.view.controller import articleController


def createApp() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container
    app.include_router(
        articleController.router,
        prefix='/article',
        tags=['Articles']
    )

    return app


app = createApp()


@app.get("/")
def index():
    return {"docs": "/docs"}
