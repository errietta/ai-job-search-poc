from typing import Optional

from fastapi import APIRouter, Query
from sqlalchemy import Integer

from db import SessionLocal
from models import EmploymentTypeEnum, ExperienceLevelEnum, Job

router = APIRouter()


@router.get("/jobs")
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
