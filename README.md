# 🎓 Assistente Pedagógico com RAG

> **Upgrade do projeto [Chat-LLM-com-RAG](https://github.com/eduardopetrocchi/Chat-LLM-com-RAG)**
> Nesta versão, a interface de **chat foi substituída por formulários**, simplificando a interação e reduzindo o consumo de tokens.

Um assistente baseado em **LangChain + RAG (Retrieval-Augmented Generation)** que auxilia professores do Ensino Fundamental I na criação de **planos de aula, listas de exercícios e provas**, fundamentados em documentos pedagógicos nas diretrizes da **BNCC**.

---

## 📌 Diferenças em relação à versão anterior

| Aspecto | Chat-LLM-com-RAG (v1) | Assistente Pedagógico (v2) |
|---|---|---|
| Interface | Chat livre com histórico | Formulário estruturado |
| Consumo de tokens | Alto (histórico completo em cada turno) | Baixo (prompt único e direto) |
| Exportação | Somente tela | Arquivo `.docx` gerado automaticamente |
| LLM suportado | Groq + Ollama (local) | Groq + Mistral AI |
| Disciplinas | Genérico | 5 matérias com prompts especializados |

---

## 🏗️ Arquitetura

```
professor_streamlit.py      ← Interface Streamlit (formulário)
│
├── services/
│   ├── prompt_selector.py  ← Seleciona o prompt da matéria
│   ├── pdf_searcher.py     ← Localiza PDFs na pasta de dados
│   └── pdf_text_extractor.py ← Extrai texto dos PDFs (PyMuPDF4LLM)
│
├── rag/
│   ├── ingest.py           ← Divide textos em chunks
│   ├── config.py           ← Cria e persiste o vectorstore Chroma
│   └── retriever.py        ← Carrega o retriever (inicializa o RAG)
│
├── tools/
│   └── recovery_tool.py    ← Cria a ferramenta RAG para o agente LangChain
│
├── agente/
│   └── agente_assistente.py ← Agente LangChain com acesso à ferramenta RAG
│
├── models/
│   └── model_loader.py     ← Carrega o LLM (Groq ou Mistral)
│
├── prompts/
│   ├── matematica_prompt.py
│   ├── portugues_prompt.py
│   ├── ciencias_prompt.py
│   ├── informatica_prompt.py
│   └── ed_fisica_prompt.py
│
└── data/
    ├── pdfs/               ← Coloque aqui os PDFs educacionais
    └── vectorstore/         ← Banco vetorial Chroma (gerado automaticamente)
```

---

## ⚙️ Fluxo de funcionamento

1. O professor preenche o formulário (matéria, série, tópico, objetivo, assunto)
2. O sistema monta um **prompt especializado** para a matéria escolhida
3. O **agente LangChain** recebe o prompt e consulta a **ferramenta RAG** (`retriever_docs`)
4. O RAG busca trechos relevantes dos PDFs educacionais indexados no **Chroma DB**
5. O LLM (Groq ou Mistral) gera o documento em **Markdown**
6. O resultado é exibido na tela e exportado automaticamente como **arquivo `.docx`**

---

## ⚠️ Atualização dos documentos PDF

> [IMPORTANTE]
> **Sempre que um novo arquivo PDF for inserido na pasta `data/pdfs/`, é necessário excluir o diretório `data/vectorstore/` antes de reiniciar a aplicação.**
>
> Isso força o sistema a re-indexar todos os documentos e incluir o novo conteúdo na base vetorial.

```bash
# Apagar o banco vetorial existente
rm -rf data/vectorstore/

# Reiniciar a aplicação — a re-indexação ocorre automaticamente na inicialização
streamlit run professor_streamlit.py
```

> [NOTA]
> A re-indexação é feita automaticamente na primeira execução (ou quando o `vectorstore` não existe).
> Isso pode levar alguns minutos dependendo do volume de PDFs.

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.10+
- [Pandoc](https://pandoc.org/installing.html) instalado no sistema (necessário para gerar `.docx`)
- Chave de API configurada no arquivo `.env`

### 1. Clone o repositório

```bash
git clone https://github.com/eduardopetrocchi/assistente-professor-rag.git
cd assistente-professor-rag
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_groq_aqui
MISTRAL_API_KEY=sua_chave_mistral_aqui   # opcional
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicione os PDFs educacionais

Coloque os arquivos PDF na pasta `data/pdfs/`:

```
data/
└── pdfs/
    ├── bncc_ensino_fundamental.pdf
    ├── curriculo_matematica.pdf
    └── ...
```

### 5. Execute a aplicação

```bash
streamlit run professor_streamlit.py
```

A aplicação estará disponível em: **http://localhost:8501**

---

## 🐳 Executar com Docker

### Build e subida com Docker Compose

```bash
docker compose up --build
```

A aplicação estará disponível em: **http://localhost:8501**

### Notas importantes sobre Docker

- Os PDFs devem estar em `./data/pdfs/` — a pasta é montada como volume no container
- Os documentos `.docx` gerados ficam disponíveis em `./resultados/` na máquina host
- O banco vetorial (`./data/vectorstore/`) é persistido entre reinicializações do container

> [AVISO]
> Ao adicionar novos PDFs, além de excluir `data/vectorstore/`, é necessário **reiniciar o container**:
> ```bash
> docker compose restart
> ```

---

## 📝 Matérias e objetivos suportados

| Matéria | Tópicos disponíveis |
|---|---|
| Matemática | Soma, Subtração, Multiplicação, Divisão |
| Português | Alfabetização, Letramento, Ortografia, Gêneros |
| Ciências da Natureza | Ecossistemas, Corpo, Matéria, Universo |
| Informática | Cidadania, Programação, Pesquisa, Hardware |
| Ed. Física | Esportes, Jogos, Corpo, Dança |

**Objetivos disponíveis:** Plano de aula · Lista de exercícios · Provas

---

## 🧪 Testes

```bash
pytest tests/ -v
```

Os testes cobrem:
- `test_ingest.py` — Divisão de textos em chunks (split)
- `test_pdf_extractor.py` — Extração de texto dos PDFs (com mock)
- `test_retriever.py` — Lógica do retriever Chroma (com mock)
- `test_tools.py` — Agente, ferramenta RAG e seletor de prompts (com mock)

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| [LangChain](https://python.langchain.com/) | Orquestração do agente e RAG |
| [Streamlit](https://streamlit.io/) | Interface web |
| [Chroma DB](https://www.trychroma.com/) | Banco de dados vetorial |
| [HuggingFace Embeddings](https://huggingface.co/) | Modelo de embeddings (`all-mpnet-base-v2`) |
| [PyMuPDF4LLM](https://pymupdf.readthedocs.io/) | Extração de texto de PDFs |
| [Groq](https://console.groq.com/) | LLM principal (`llama-3.3-70b-versatile`) |
| [Mistral AI](https://mistral.ai/) | LLM alternativo |
| [pypandoc](https://github.com/NicklasTegner/pypandoc) | Conversão Markdown → `.docx` |
| [pytest](https://pytest.org/) | Testes unitários e de integração |

---

## 📂 Estrutura de saída

Os documentos gerados são salvos automaticamente em:

```
resultados/
├── plano_aula/
│   └── plano_aula-04082026-161027.docx
├── lista_exercicios/
│   └── lista_exercicios-04082026-161844.docx
└── prova/
    └── prova-04082026-162100.docx
```

---

## 📄 Licença

MIT License — sinta-se livre para usar, modificar e distribuir.
