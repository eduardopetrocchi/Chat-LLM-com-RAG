# ============================================================
# Dockerfile — Assistente Pedagógico com RAG
# ============================================================
# Imagem base: Python 3.10 slim (compatível com llm_env)
FROM python:3.10-slim

# Metadados da imagem
LABEL maintainer="eduardopetrocchi"
LABEL description="Assistente Pedagógico com RAG — LangChain + Streamlit"

# Evita prompts interativos durante o build
ENV DEBIAN_FRONTEND=noninteractive

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# ── Dependências do sistema ──────────────────────────────────
# pandoc: necessário para conversão Markdown → .docx (pypandoc)
# build-essential: necessário para compilar alguns pacotes Python nativos
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Dependências Python ──────────────────────────────────────
# Copia primeiro apenas o requirements para aproveitar o cache de layers do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Código da aplicação ──────────────────────────────────────
COPY . .

# Cria os diretórios de dados e resultados esperados pela aplicação
RUN mkdir -p data/pdfs data/vectorstore resultados/plano_aula resultados/lista_exercicios resultados/prova

# Porta padrão do Streamlit
EXPOSE 8501

# Healthcheck para monitorar se a aplicação está respondendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── Comando de inicialização ─────────────────────────────────
CMD ["streamlit", "run", "professor_streamlit.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
