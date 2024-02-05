# Образ Python
FROM python:3.12.1

RUN pip install poetry
WORKDIR /app

COPY configs/ /app/configs
COPY data/ /app/data
COPY quotes/ /app/quotes
# COPY .env /app/.env
COPY .env /app/.env
COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml

RUN poetry install

EXPOSE 8000
# CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
