# Use uma imagem base oficial do Python com Alpine Linux
FROM python:3.12-slim-bookworm AS builder


# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copia o arquivo requirements.txt para o container
COPY requirements.txt ./

# Instala o uv e as dependências do requirements.txt
RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Define as variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Define o usuário não root para executar a aplicação
USER appuser

# Define o comando para executar a aplicação
CMD ["python", "-m", "flask", "run"]