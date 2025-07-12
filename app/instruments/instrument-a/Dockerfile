FROM python:3.9-slim

WORKDIR /app

RUN pip install Flask requests \
    && useradd --no-log-init --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

COPY app.py .

CMD ["python", "app.py"]
