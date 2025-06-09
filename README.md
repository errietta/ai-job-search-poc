# Job Search FastAPI Project

This project is a FastAPI application with a PostgreSQL database, managed using Docker Compose and Alembic for migrations.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Python 3.11+](https://www.python.org/downloads/)

## Getting Started

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd job-search
```

### 2. Start the services (API + Postgres)

```sh
docker compose up --build
```

This will start both the FastAPI app and a Postgres database. The API will be available at [http://localhost:8000](http://localhost:8000).

### 3. Install dependencies (for migrations/scripts)

```sh
poetry install
```

### 4. Create and run migrations

#### a. Create a new migration (after editing models)

```sh
poetry run alembic revision --autogenerate -m "your migration message"
```

#### b. Apply migrations to the database

```sh
poetry run alembic upgrade head
```

### 5. Populate the database with dummy jobs

```sh
poetry run python populate_jobs.py 100
```

This will insert 100 fake jobs. You can change the number as needed.

### 6. Cleaning up salary data (if needed)

If you change the `salary` field to integer, clean up old data:

```sh
docker compose exec postgres psql -U user -d jobsearch -c "UPDATE jobs SET salary = regexp_replace(salary, '[^0-9]', '', 'g') WHERE salary IS NOT NULL;"
```

## Useful Commands

- View API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Stop services: `docker compose down`

## Troubleshooting

- If you get errors about database connection, make sure Postgres is healthy (`docker compose ps`).
- If you get migration errors about types, clean up the data as shown above.

---

For more, see the code and comments in each file.
