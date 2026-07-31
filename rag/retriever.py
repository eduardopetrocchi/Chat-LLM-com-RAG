"""
Módulo do Retriever (retriever.py)
----------------------------------
Carrega o banco de vetores ChromaDB existente e o expõe como um retriever.
Caso o banco de vetores não exista localmente, o módulo executa automaticamente
o pipeline de ingestão de documentos (ingest.py) antes de retornar o retriever.
Usa o algoritmo MMR (Maximal Marginal Relevance) para o retriever.
"""

from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from rag.ingest import config_retriever


EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
VECTOR_PATH = "/app/data/vectorstore/index_chromaDB_professores"
FOLDER_PATH = "/app/data/pdfs"

def get_retriever(folder_path=FOLDER_PATH, vector_path=VECTOR_PATH, k=3, fetch_k=4):
    """
    Carrega o ChromaDB a partir do caminho fornecido. Se o diretório não existir,
    inicia a ingestão automática dos PDFs localizados na pasta de dados padrão.

    Parâmetros:
        vector_path (str): Diretório onde o banco ChromaDB está ou deve ser armazenado.
        k (int): Quantidade de documentos relevantes a retornar. Default: 3.
        fetch_k (int): Quantidade de documentos preliminares a selecionar para o MMR. Default: 4.

    Retorna:
        Retriever do LangChain configurado para recuperação semântica via MMR.
    """

    # Inicializa o mesmo modelo de embeddings usado na criação do banco
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Se o banco de vetores não existir, realiza a ingestão e vetorização automática
    if not Path(vector_path).exists():
        print(
            f"Vectorstore não encontrado em '{vector_path}'. Indexando documentos automaticamente..."
        )
        vectorstore = config_retriever(folder_path, vector_path)
    else:
        # Carrega a instância do ChromaDB persistido
        print(f"Vectorstore encontrado em '{vector_path}'. Carregando...")
        vectorstore = Chroma(
            persist_directory=vector_path,
            embedding_function=embeddings,
        )

    # Configura o retriever usando MMR (Maximal Marginal Relevance)
    # MMR reduz redundância selecionando documentos relevantes que sejam diversos entre si
    retriever = vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": k, "fetch_k": fetch_k}
    )

    return retriever
