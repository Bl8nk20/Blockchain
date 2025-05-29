FROM python:3.12-slim

WORKDIR /app

# Install basic dependencies
RUN apt-get update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY api/ ./api/
COPY tests/ ./tests/

ENV PYTHONPATH="/app"

ENTRYPOINT ["python", "api/application.py"]
