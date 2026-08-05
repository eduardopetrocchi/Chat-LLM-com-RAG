from typing import List
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from services.pdf_text_extractor import extract_text_pdf
from services.pdf_searcher import find_pdfs
from rag.ingest import split_documents

EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"


def config_retriever(folder_path: str, vector_path: str) -> Chroma:
    """Processa os arquivos PDF contidos na pasta especificada e constrói o banco vetorial Chroma DB.

    Nota: Se novos PDFs forem adicionados em 'data/pdfs', o diretório 'data/vectorstore' (vectorstore)
    deve ser excluído para forçar a re-indexação completa dos documentos.

    Args:
        folder_path (str): Caminho do diretório contendo os arquivos PDF.
        vector_path (str): Caminho do diretório onde o banco vetorial será persistido.

    Returns:
        Chroma: Objeto vectorstore Chroma configurado com os documentos indexados.
    """
    pdf_files: List[Path] = find_pdfs(folder_path)

    # Extrai o texto contínuo de cada PDF encontrado
    loaded_documents: List[str] = [extract_text_pdf(str(pdf)) for pdf in pdf_files]

    # Divide os textos em chunks para melhor recuperação semântica
    chunks: List[str] = split_documents(loaded_documents)

    # Instancia os embeddings HuggingFace e cria a base vetorial Chroma
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore: Chroma = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=vector_path,
    )

    print("Documentos vetorados e indexados no Chroma DB com sucesso!")
    return vectorstore
