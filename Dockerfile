# Usa uma imagem base oficial do Python
FROM python:3.12-slim-bookworm AS builder

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema necessárias para Pillow e fontes
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements.txt
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Define variáveis de ambiente (se precisar para rodar Flask, mas nesse caso tá rodando direto com app.py)
ENV PYTHONUNBUFFERED=1

# Porta (caso queira explicitar, mas o Waitress já roda em 0.0.0.0:5050)
EXPOSE 5050

# Comando para iniciar a aplicação
CMD ["python", "app/app.py"]
