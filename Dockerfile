# CTF Vulnerability Suite Dockerfile
# WARNING: This container contains intentional security vulnerabilities
# Use only in isolated CTF environments - DO NOT expose to the internet!

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY seed_db.py .

# Create database directory and set permissions
RUN mkdir -p /app/data

# Seed the database
RUN python seed_db.py

# Create non-root user for security (though app is intentionally vulnerable)
RUN useradd -m -u 1000 ctfuser && chown -R ctfuser:ctfuser /app
USER ctfuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "app:app"]
