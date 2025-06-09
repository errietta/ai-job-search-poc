from models import Job, EmploymentTypeEnum, ExperienceLevelEnum
from main import SessionLocal
from faker import Faker
import random


def populate_jobs(n=100):
    fake = Faker()
    jobs = []
    for _ in range(n):
        job = Job(
            title=fake.job(),
            company=fake.company(),
            company_employee_count=random.randint(10, 10000),
            location=fake.city(),
            description=fake.text(max_nb_chars=200),
            salary=f"${random.randint(40000, 200000)}",
            url=fake.url(),
            date_posted=str(fake.date_this_year()),
            job_type=random.choice(["permanent", "temporary", "contract"]),
            experience_level=random.choice(list(ExperienceLevelEnum)),
            employment_type=random.choice(list(EmploymentTypeEnum)),
            remote=random.choice([True, False]),
            hybrid=random.choice([True, False]),
            industry=fake.bs(),
        )
        jobs.append(job)
    with SessionLocal() as session:
        session.bulk_save_objects(jobs)
        session.commit()
    print(f"Inserted {n} jobs.")


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    populate_jobs(n)
