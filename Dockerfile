FROM python:3.12-slim-bookworm

WORKDIR /app

# Instala as libs necessárias pro Pillow funcionar corretamente
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

# Copia dependências
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Define variáveis do Flask (por precaução)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050

# Expõe a porta usada no app
EXPOSE 5050

# Usa usuário seguro
USER appuser

# Roda o app com waitress (modo produção)
CMD ["python", "app.py"]
