# Base stage: Install dependencies
FROM python:3.12-alpine as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies in one layer
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --default-timeout=10000 -r requirements.txt

# Final stage: Build the web and celery services
FROM python:3.12-alpine

# Copy installed dependencies from the base stage
COPY --from=base /usr/lib/python3.12/site-packages /usr/lib/python3.12/site-packages
COPY --from=base /opt/venv /opt/venv

# Set environment variables for the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app/

# Set up entry point for the Django web service (adjust as necessary for Celery)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]