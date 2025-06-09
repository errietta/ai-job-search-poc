from pydantic import BaseModel, Field


class JobFilter(BaseModel):
    """
    Filter for job listings.
    """

    title__ilike: str = Field(
        default=None,
        description="Filter jobs by title using case-insensitive partial match.",
    )
    company__ilike: str = Field(
        default=None,
        description="Filter jobs by company using case-insensitive partial match.",
    )
    location__ilike: str = Field(
        default=None,
        description="Filter jobs by location using case-insensitive partial match.",
    )
    employment_type: str = Field(
        default=None,
        description="Filter jobs by employment type (e.g., full_time, part_time, contract).",
        examples=[
            "full_time",
            "part_time",
            "contract",
        ],
    )
    experience_level: str = Field(
        default=None,
        description="Filter jobs by experience level (e.g., entry_level, mid_level, senior_level).",
        examples=[
            "entry_level",
            "mid_level",
            "senior_level",
            "director",
            "executive",
            "internship",
            "other",
        ],
    )
    remote: bool = Field(
        default=None,
        description="Filter jobs by remote work availability.",
    )
    hybrid: bool = Field(
        default=None,
        description="Filter jobs by hybrid work availability.",
    )
    industry__ilike: str = Field(
        default=None,
        description="Filter jobs by industry using case-insensitive partial match.",
    )
    salary__gte: int = Field(
        default=None,
        description="Filter jobs by minimum salary.",
    )
    company_size: str = Field(
        default=None,
        description="Filter jobs by company size",
        examples=[
            "small",
            "medium",
            "large",
            "enterprise",
        ],
    )
