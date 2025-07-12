#!/bin/bash
cd /app
poetry run cel8ry -A laf.tasks.celery worker --loglevel=info
