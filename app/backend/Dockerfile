FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root \
    && useradd --no-log-init --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app \
    && chmod +x celery_worker.sh

USER appuser

ENV PYTHONPATH=/app/src

#ENTRYPOINT ["/app/celery_worker.sh"]
