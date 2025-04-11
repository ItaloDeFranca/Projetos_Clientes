FROM python:3.12-slim-bookworm

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria o usuário não-root
RUN useradd -m appuser

# Copia os arquivos da aplicação
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050

# Troca para usuário não-root
USER appuser

# Expõe a porta usada pela app
EXPOSE 5050

# Comando para rodar com waitress (modo produção)
CMD ["python", "app.py"]
