from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    loaded_documents: List[str], chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[str]:
    """Divide uma lista de textos carregados em fragmentos (chunks) menores.

    Args:
        loaded_documents (List[str]): Lista de textos extraídos dos PDFs.
        chunk_size (int): Tamanho máximo de cada fragmento em caracteres. Padrão 1000.
        chunk_overlap (int): Sobreposição de caracteres entre fragmentos consecutivos. Padrão 200.

    Returns:
        List[str]: Lista de fragmentos de texto prontos para vetorização.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    chunks: List[str] = []
    for doc in loaded_documents:
        chunks.extend(text_splitter.split_text(doc))

    return chunks
