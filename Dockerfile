# syntax=docker/dockerfile:1.2
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY challenge/ .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]