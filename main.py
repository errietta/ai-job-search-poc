from fastapi import FastAPI, Query
from sqlalchemy import Integer, create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional
import json
import os
import logging

logger = logging.getLogger(__name__)

# Alembic uses this for migrations
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/jobsearch"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

Base = declarative_base()


@app.on_event("startup")
def startup():
    # Test DB connection on startup
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        import sys

        print(f"Database connection failed: {e}", file=sys.stderr)
        raise


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/jobs")
def read_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    employment_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    remote: Optional[bool] = None,
    hybrid: Optional[bool] = None,
    industry: Optional[str] = None,
    min_salary: Optional[int] = None,
):
    with SessionLocal() as session:
        from models import Job, EmploymentTypeEnum, ExperienceLevelEnum

        query = session.query(Job)
        if title:
            query = query.filter(Job.title.ilike(f"%{title}%"))
        if company:
            query = query.filter(Job.company.ilike(f"%{company}%"))
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))
        if employment_type:
            try:
                query = query.filter(
                    Job.employment_type == EmploymentTypeEnum[employment_type]
                )
            except KeyError:
                pass
        if experience_level:
            try:
                query = query.filter(
                    Job.experience_level == ExperienceLevelEnum[experience_level]
                )
            except KeyError:
                pass
        if remote is not None:
            query = query.filter(Job.remote == remote)
        if hybrid is not None:
            query = query.filter(Job.hybrid == hybrid)
        if industry:
            query = query.filter(Job.industry.ilike(f"%{industry}%"))
        if min_salary is not None:
            query = query.filter(Job.salary.cast(Integer) >= min_salary)

        jobs = query.offset(skip).limit(limit).all()

        return [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "company_employee_count": job.company_employee_count,
                "location": job.location,
                "description": job.description,
                "salary": job.salary,
                "url": job.url,
                "date_posted": job.date_posted,
                "job_type": job.job_type,
                "experience_level": (
                    job.experience_level.name if job.experience_level else None
                ),
                "employment_type": (
                    job.employment_type.name if job.employment_type else None
                ),
                "remote": job.remote,
                "hybrid": job.hybrid,
                "industry": job.industry,
            }
            for job in jobs
        ]


@app.get("/jobs-ai-search")
def read_jobs_ai_search(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    filter: Optional[str] = None,
):
    from models import Job

    # Parse filter string as dict
    # if filter:
    #    try:
    #        filter_dict = json.loads(filter)
    #    except Exception:
    #        filter_dict = {}
    # else:

    logger.warning(f"Received filter: {filter}")

    filter_dict = {}

    with SessionLocal() as session:
        query = session.query(Job)
        for key, value in filter_dict.items():
            if "__" in key:
                field, op = key.split("__", 1)
                col = getattr(Job, field, None)
                if not col:
                    continue
                if op == "ilike":
                    query = query.filter(col.ilike(f"%{value}%"))
                elif op == "eq":
                    query = query.filter(col == value)
                elif op == "gte":
                    query = query.filter(col.cast(Integer) >= value)
                elif op == "lte":
                    query = query.filter(col.cast(Integer) <= value)
            else:
                col = getattr(Job, key, None)
                if not col:
                    continue
                query = query.filter(col == value)

        jobs = query.offset(skip).limit(limit).all()

        return [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "company_employee_count": job.company_employee_count,
                "location": job.location,
                "description": job.description,
                "salary": job.salary,
                "url": job.url,
                "date_posted": job.date_posted,
                "job_type": job.job_type,
                "experience_level": (
                    job.experience_level.name if job.experience_level else None
                ),
                "employment_type": (
                    job.employment_type.name if job.employment_type else None
                ),
                "remote": job.remote,
                "hybrid": job.hybrid,
                "industry": job.industry,
            }
            for job in jobs
        ]
