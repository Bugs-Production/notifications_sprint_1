import uvicorn
from celery import Celery
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

celery_app = Celery(settings.project_name, broker=settings.broker_url)

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

add_pagination(app)

# Для локального запуска
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
