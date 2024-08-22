# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Load environment variables
RUN export $(cat .env | xargs)

# Install build tools
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Run database migrations and collect static files
RUN python manage.py collectstatic --noinput

# # Command to run the Gunicorn server
# CMD ["gunicorn", "config:application", "--bind", "0.0.0.0:$PORT"]