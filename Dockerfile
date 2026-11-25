# Use a lightweight, official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker's caching system
COPY requirements.txt .

# Install Flask and dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Gunicorn will listen on port 5000 inside the container
EXPOSE 5000

# Run Gunicorn, binding to all network interfaces inside the container network
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]

