from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from models import Job, EmploymentTypeEnum, ExperienceLevelEnum
from faker import Faker
import random

# revision identifiers, used by Alembic.
revision = "populate_jobs_with_fixtures"
down_revision = "4b6616730381"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    fake = Faker()
    jobs = []
    for _ in range(100):
        job = Job(
            title=fake.job(),
            company=fake.company(),
            company_employee_count=random.randint(10, 10000),
            location=fake.city(),
            description=fake.text(max_nb_chars=200),
            salary=f"{random.randint(40000, 200000)}",
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
    session.bulk_save_objects(jobs)
    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.query(Job).delete()
    session.commit()
    session.close()
