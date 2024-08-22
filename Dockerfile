# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Environment variables for database
ENV DATABASE_PORT='5432'
ENV DATABASE_NAME='voice_writer'
ENV DATABASE_USER='vwadmin'
ENV DATABASE_PASSWORD='spyglass_home_HOMEMADE_chinch'
ENV DATABASE_URL='postgres://${DATABASE_USER}:${DATABASE_PASSWORD}@$db:${DATABASE_PORT}/${DATABASE_NAME}'

# Run database migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Command to run the Gunicorn server
CMD ["gunicorn", "config:application", "--bind", "0.0.0.0:$PORT"]