# Usa imagem leve com Python
FROM python:3.12-slim-bookworm

# Cria diretório de trabalho
WORKDIR /app

# Instala dependências de sistema necessárias pro Pillow + fontes
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tudo (inclusive /app/app.py e images)
COPY . .

# Seta variável pra evitar buffer no log
ENV PYTHONUNBUFFERED=1

# Expõe a porta usada no app
EXPOSE 5050

# Comando de start (o app.py tá dentro da pasta /app)
CMD ["python", "app/app.py"]
