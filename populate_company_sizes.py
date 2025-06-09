from models import CompanySize
from db import SessionLocal


def populate_company_sizes():
    sizes = [
        {"size": "Small", "min_employees": 1, "max_employees": 50},
        {"size": "Medium", "min_employees": 51, "max_employees": 250},
        {"size": "Large", "min_employees": 251, "max_employees": 1000},
        {"size": "Enterprise", "min_employees": 1001, "max_employees": None},
    ]
    with SessionLocal() as session:
        for s in sizes:
            exists = session.query(CompanySize).filter_by(size=s["size"]).first()
            if not exists:
                cs = CompanySize(**s)
                session.add(cs)
        session.commit()
    print("Company sizes populated.")


if __name__ == "__main__":
    populate_company_sizes()
