FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin script dan data
COPY src/ ./src/
COPY data/ ./data/

# Jalankan script saat container start
CMD ["python", "src/etl.py"]
