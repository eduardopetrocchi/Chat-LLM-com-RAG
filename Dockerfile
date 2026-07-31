FROM python:3.11-slim

# Evita a gravação de arquivos .pyc no disco e força a saída de logs diretamente para o terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências essenciais do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código fonte
COPY . .

# Garante que as pastas de dados persistidos existam
RUN mkdir -p /app/data/pdfs /app/data/vectorstore

# Define a execução do assistente via terminal como ponto de entrada principal
CMD ["python", "main.py"]

