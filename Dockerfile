# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy entire project structure (includes pre-generated data)
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8080}