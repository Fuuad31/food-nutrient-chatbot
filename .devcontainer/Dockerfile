# .devcontainer/Dockerfile
FROM python:3.11-slim
# --- TAMBAHKAN BARIS DI BAWAH INI ---
# Update package lists and install git
RUN apt-get update && apt-get install -y git

WORKDIR /workspace

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt