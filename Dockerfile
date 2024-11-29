# Use official Python image as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port the application will run on
EXPOSE 8000

# Run database migrations and collect static files
RUN python manage.py collectstatic --noinput && \
    python manage.py makemigrations && \
    python manage.py migrate

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
