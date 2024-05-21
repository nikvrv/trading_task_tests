# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the source files to the working directory
COPY . /app

# Install system dependencies and create a virtual environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Default command to run tests
ENTRYPOINT ["sh", "-c", "pytest --dist loadscope -n 4"]
