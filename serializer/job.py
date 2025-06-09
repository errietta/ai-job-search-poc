def format_jobs(jobs):
    results = [
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

    return results
