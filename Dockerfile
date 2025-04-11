FROM python:3.12-slim-bookworm

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Cria o usuário não-root
RUN useradd -m appuser

# Copia requirements e instala dependências
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação
COPY . .

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Troca para usuário não-root
USER appuser

# Comando para iniciar a aplicação
CMD ["flask", "run"]
