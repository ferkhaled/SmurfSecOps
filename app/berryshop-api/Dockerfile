# Start from a small official Python image.
FROM python:3.12-slim

# Keep Python output visible in container logs and avoid `.pyc` clutter.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to improve layer reuse when source code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application source needed at runtime.
COPY src ./src

# Run as a non-root user to model a safer default.
RUN useradd --create-home --shell /usr/sbin/nologin berryshop
USER berryshop

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
