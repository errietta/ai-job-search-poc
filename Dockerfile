# Use official Python image with 3.11
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock README.md ./
COPY main.py ./

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
