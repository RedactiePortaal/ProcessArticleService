import uvicorn
from fastapi import FastAPI

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
