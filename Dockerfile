# Use official Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app
COPY . .
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV ENV=dlocal

# Install system dependencies (optional)
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    gcc \
    python3-dev \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (for caching)
# COPY requirements.txt .

# Install dependencies
RUN cd radna-accounting-service && pip install --upgrade pip
RUN cd radna-accounting-service && pip install --no-cache-dir -r requirements.txt

# Copy project files

# Default command (adjust to your app)
CMD ["python", "./radna-accounting-service/manage.py", "runserver", "0.0.0.0:8000"]