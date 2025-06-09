from fastapi import APIRouter, Query
from typing import Optional
import logging

from models import Job
from util.filter import get_llm_job_filters
from util.pagination import get_pagination_urls
from util.query import query_dict_to_sqlalchemy
from serializer.job import format_jobs
from db import SessionLocal

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/jobs-ai-search")
def read_jobs_ai_search(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    filter: Optional[str] = None,
):
    logger.warning(f"Received filter: {filter}")
    with SessionLocal() as session:
        query = session.query(Job)
        filter_dict = get_llm_job_filters(filter)
        logger.warning(f"Parsed filter dict: {filter_dict}")

        query = query_dict_to_sqlalchemy(Job, query, filter_dict)
        total = query.count()
        jobs = query.offset(skip).limit(limit).all()
        next_page, prev_page = get_pagination_urls(
            "/jobs-ai-search", skip, limit, filter, total
        )

        results = format_jobs(jobs)
        return {
            "total": total,
            "next_page": next_page,
            "prev_page": prev_page,
            "results": results,
        }
