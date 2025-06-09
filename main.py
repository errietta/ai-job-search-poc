from fastapi import FastAPI

import logging

from routes.jobs.search_jobs import router as search_jobs_router
from routes.jobs.search_jobs_ai import router as ai_router

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(search_jobs_router)
app.include_router(ai_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
