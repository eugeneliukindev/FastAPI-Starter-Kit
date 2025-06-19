FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip wheel "poetry==2.1.3"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry lock && \
    poetry install --only main --no-root --no-interaction && \
    pip uninstall -y poetry

COPY src/ src/
COPY migrations/ migrations/
COPY scripts/ scripts/
COPY src/main.py alembic.ini ./

RUN chmod +x scripts/prestart-migrations.sh scripts/startup-gunicorn

ENTRYPOINT ["scripts/prestart-migrations.sh"]
CMD ["scripts/startup-gunicorn"]
