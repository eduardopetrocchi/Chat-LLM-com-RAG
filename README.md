# Sidekick Professores

Assistente virtual de **RAG** (Retrieval-Augmented Generation) para responder perguntas sobre documentos PDF. O projeto indexa materiais didáticos, recupera trechos relevantes com busca semântica e gera respostas contextualizadas via LLM, com suporte a histórico de conversa.

## Funcionalidades

- **Ingestão automática de PDFs** — na primeira execução, varre `data/pdfs/`, extrai o texto e cria o índice vetorial no ChromaDB.
- **RAG com histórico** — usa um retriever *history-aware* para reformular perguntas que dependem do contexto da conversa (ex.: "e ele?").
- **Recuperação MMR** — Maximal Marginal Relevance reduz trechos redundantes nas respostas.
- **LLM via API** — Groq como provedor padrão (`llama-3.3-70b-versatile`), com suporte opcional à Mistral.
- **Interface CLI** — chat interativo no terminal.
- **Docker Compose** — sobe a aplicação com um único comando.

## Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  data/pdfs  │────▶│   ingest.py  │────▶│  ChromaDB       │
│  (*.pdf)    │     │  (chunking)  │     │  (vectorstore)  │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
┌─────────────┐     ┌──────────────┐              │
│  Terminal   │────▶│   main.py    │◀─────────────┘
│  (CLI)      │     │  chat_agent  │     retriever (MMR)
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  LLM (API)   │
                    │  Groq /      │
                    │  Mistral     │
                    └──────────────┘
```

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/)
- Chave de API da [Groq](https://console.groq.com/keys)
- (Opcional) [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) Chave de API da [Mistral](https://console.mistral.ai/)

## Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/sidekick-professores.git
cd sidekick-professores
```

### 2. Variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` e configure sua chave da Groq:

| Variável | Descrição | Obrigatória |
|---|---|---|
| `GROQ_API_KEY` | Chave da API Groq | Sim |
| `MISTRAL_API_KEY` | Chave da API Mistral (alternativa ao Groq) | Não |
| `HF_TOKEN` | Token HuggingFace (downloads de embeddings) | Não |

### 3. Adicionar documentos PDF

Coloque os arquivos `.pdf` em `data/pdfs/`:

```bash
cp /caminho/para/seu/material.pdf data/pdfs/
```

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
python main.py
```

Na primeira execução, se o índice vetorial ainda não existir, a ingestão dos PDFs é feita automaticamente.

Digite suas perguntas no prompt `Você:`. Para encerrar, use `sair`, `exit` ou `quit` (ou `Ctrl+C` / `Ctrl+D`).

## Execução com Docker

```bash
cp .env.example .env
# Edite .env com sua GROQ_API_KEY

docker compose up --build
```

Em outro terminal, anexe-se ao container:

```bash
docker attach sidekick-professores
```

> **Dica:** para desanexar sem parar o container, use `Ctrl+P` seguido de `Ctrl+Q`.

## Trocar o provedor de LLM

Por padrão, `get_model()` usa Groq. Para usar Mistral, altere a chamada em `main.py`:

```python
llm = get_model("mistral")
```

Certifique-se de que a chave de API correspondente está definida no `.env`.

## Testes

O projeto usa [pytest](https://docs.pytest.org/) para testes unitários. As dependências externas (LLM, embeddings, ChromaDB, extração de PDF) são mockadas, então os testes rodam rápido e sem precisar de chave de API.

### Instalar dependências de teste

```bash
pip install pytest pytest-mock
```

### Rodar os testes

```bash
pytest
```

Comandos úteis:

```bash
pytest -v                                  # modo verboso
pytest tests/test_retriever.py -v          # rodar só um arquivo
pytest --cov=. --cov-report=term-missing   # ver cobertura (requer pytest-cov)
```

### Cobertura atual

| Módulo | Arquivo de teste | O que é testado |
|---|---|---|
| `services/pdf_extractor.py` | `test_pdf_extractor.py` | Extração e concatenação do texto das páginas |
| `rag/ingest.py` | `test_ingest.py` | Tamanho e overlap dos chunks |
| `rag/retriever.py` | `test_retriever.py` | Carregamento vs. reindexação do vectorstore, parâmetros do MMR |
| `agents/chat_agent.py` | `test_chat_agent.py` | Atualização do histórico de conversa e resposta do agente |

## Estrutura do projeto

```
.
├── agents/
│   └── chat_agent.py       # Loop de conversa e histórico
├── models/
│   └── model_loader.py     # Carregamento de LLMs (Groq, Mistral)
├── rag/
│   ├── config.py           # Chain RAG history-aware
│   ├── ingest.py           # Ingestão de PDFs → ChromaDB
│   ├── paths.py            # Caminhos relativos do projeto
│   ├── prompts.py          # Prompts do sistema
│   └── retriever.py        # Carregamento do retriever (MMR)
├── services/
│   ├── pdf_extractor.py    # Extração de texto com PyMuPDF4LLM
│   └── pdf_finder.py       # Busca de arquivos PDF
├── tests/
│   ├── test_chat_agent.py    # Testes do loop de conversa
│   ├── test_ingest.py        # Testes de chunking e ingestão
│   ├── test_pdf_extractor.py # Testes de extração de texto
│   └── test_retriever.py     # Testes do retriever (MMR)
├── data/
│   ├── pdfs/               # PDFs de entrada (adicionar aqui)
│   └── vectorstore/        # Índice ChromaDB persistido
├── main.py                 # Ponto de entrada (CLI)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Stack tecnológica

| Componente | Tecnologia |
|---|---|
| Orquestração RAG | LangChain |
| Banco vetorial | ChromaDB |
| Embeddings | `sentence-transformers/all-mpnet-base-v2` (HuggingFace) |
| Extração de PDF | PyMuPDF4LLM |
| LLM padrão | Groq — `llama-3.3-70b-versatile` |
| LLM alternativo | Mistral — `mistral-medium-3-5` |
| Containerização | Docker + Docker Compose |

## Parâmetros de ingestão e recuperação

| Parâmetro | Valor | Arquivo |
|---|---|---|
| Tamanho do chunk | 1000 caracteres | `rag/ingest.py` |
| Overlap do chunk | 200 caracteres | `rag/ingest.py` |
| Documentos retornados (`k`) | 3 | `rag/retriever.py` |
| Candidatos MMR (`fetch_k`) | 4 | `rag/retriever.py` |

Para reindexar após adicionar ou alterar PDFs, remova o conteúdo de `data/vectorstore/` (mantendo o `.gitkeep`) e reinicie a aplicação.

## Solução de problemas

**`GROQ_API_KEY não foi configurada`**
Copie `.env.example` para `.env` e preencha sua chave da Groq.

**O assistente não encontra PDFs**
Verifique se há arquivos `.pdf` em `data/pdfs/`.

**Erro de rate limit da Groq**
A API gratuita da Groq tem limites de requisições. Aguarde alguns segundos e tente novamente.

**Ingestão lenta na primeira execução**
O download do modelo de embeddings (`all-mpnet-base-v2`) e a vetorização dos PDFs ocorrem na primeira indexação; execuções seguintes reutilizam o índice persistido.

## Licença

Projeto educacional — consulte o repositório para informações de licenciamento.