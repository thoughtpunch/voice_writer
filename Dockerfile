# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build tools
RUN apt-get update && apt-get install -y build-essential && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --default-timeout=10000 -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/