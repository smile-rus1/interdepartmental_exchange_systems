from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.routes import router
from src.config import config
from src.services.bootstrap import create_test_transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_test_transaction()
    yield


app = FastAPI(title="Registry API", lifespan=lifespan)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        app="src.main:app",
        host=config.web.host,
        port=config.web.port,
        reload=True,
        log_level="info"
    )
