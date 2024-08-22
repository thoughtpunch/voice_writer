# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgres://vwadmin:spyglass_home_HOMEMADE_chinch@db:5432/voice_writer

# Load environment variables
RUN export $(cat .env | xargs)

# Install build tools
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Run database migrations and collect static files
RUN export $(cat .env | xargs)
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Command to run the Gunicorn server
CMD ["gunicorn", "config:application", "--bind", "0.0.0.0:$PORT"]