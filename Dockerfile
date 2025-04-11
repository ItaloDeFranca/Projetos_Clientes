FROM python:3.12-slim-bookworm

WORKDIR /app

# Instala as libs necessárias pro Pillow
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev && \
    rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd -m appuser

# Copia os arquivos
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Define variáveis
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050

EXPOSE 5050

USER appuser

# Corrigido: aponta pro app.py dentro da pasta /app/app
CMD ["python", "app/app.py"]
