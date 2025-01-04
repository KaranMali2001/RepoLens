# Stage 1: Build dependencies
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim as runtime

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup --system appgroup && \
    adduser --system --group appuser

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages from wheels
RUN pip install --no-cache /wheels/*

# Set environment variables before copying code
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy the application
COPY ./app /app/app
COPY ./main.py /app/main.py

# Make sure all directories are readable by the non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start the application
WORKDIR /app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]