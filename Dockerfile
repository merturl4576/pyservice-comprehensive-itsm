FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (PostgreSQL only, no MySQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyservice/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY pyservice/ .

# Collect static files (SECRET_KEY placeholder for build time only)
RUN SECRET_KEY=build-time-placeholder python manage.py collectstatic --noinput || true

EXPOSE 8000

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
