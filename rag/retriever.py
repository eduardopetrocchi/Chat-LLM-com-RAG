import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from rag.config import config_retriever

EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
VECTOR_PATH: str = "data/vectorstore/"
FOLDER_PATH: str = "data/pdfs/"

# Garante a existência dos diretórios padrão de entrada e banco de dados
os.makedirs(VECTOR_PATH, exist_ok=True)
os.makedirs(FOLDER_PATH, exist_ok=True)


def get_retriever(
    folder_path: str = FOLDER_PATH,
    vector_path: str = VECTOR_PATH,
    k: int = 3,
    fetch_k: int = 4,
) -> VectorStoreRetriever:
    """Carrega ou inicializa o banco de dados vetorial Chroma e retorna um recuperador (retriever) configurado.

    IMPORTANTE: Caso novos arquivos PDF sejam adicionados no diretório 'data/pdfs',
    é necessário remover o diretório 'data/vectorstore' (vectorstore) para que o sistema
    re-indexe todos os documentos na próxima execução.

    Args:
        folder_path (str): Pasta contendo os PDFs educacionais. Padrão 'data/pdfs/'.
        vector_path (str): Pasta onde o banco vetorial está persistido. Padrão 'data/vectorstore/'.
        k (int): Número de documentos relevantes a serem retornados no MMR. Padrão 3.
        fetch_k (int): Número total de candidatos a recuperar para diversificação no MMR. Padrão 4.

    Returns:
        VectorStoreRetriever: Recuperador configurado com busca por MMR (Maximal Marginal Relevance).
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Se a pasta do vectorstore não existir ou estiver vazia, realiza a ingestão e indexação inicial
    if not Path(vector_path).exists() or not os.listdir(vector_path):
        print("Vectorstore não encontrado ou vazio. Indexando documentos PDF...")
        vectorstore = config_retriever(folder_path, vector_path)
    else:
        vectorstore = Chroma(
            persist_directory=vector_path,
            embedding_function=embeddings,
        )

    retriever: VectorStoreRetriever = vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": k, "fetch_k": fetch_k}
    )

    return retriever


# Instância global do retriever pronta para uso pelas ferramentas do agente
retriever: VectorStoreRetriever = get_retriever()
