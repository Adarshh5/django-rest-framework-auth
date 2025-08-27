FROM python:3.12-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# System deps (needed for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary whitenoise

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn with 4 workers
CMD exec gunicorn SimpleInvoice.wsgi:application \
    --bind :$PORT \
    --workers 4 \
    --threads 2 \
    --timeout 120
