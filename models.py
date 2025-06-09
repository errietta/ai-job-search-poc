from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from main import Base


class EmploymentTypeEnum(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"


class ExperienceLevelEnum(enum.Enum):
    entry_level = "entry_level"
    mid_level = "mid_level"
    senior_level = "senior_level"
    director = "director"
    executive = "executive"
    internship = "internship"
    other = "other"


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    company_employee_count = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    url = Column(String, nullable=True)
    date_posted = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    experience_level = Column(Enum(ExperienceLevelEnum), nullable=True)
    employment_type = Column(Enum(EmploymentTypeEnum), nullable=True)
    remote = Column(Boolean, nullable=True)
    hybrid = Column(Boolean, nullable=True)
    industry = Column(String, nullable=True)
