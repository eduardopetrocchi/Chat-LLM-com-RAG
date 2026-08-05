from typing import List
from rag.ingest import split_documents


def test_split_documents_respects_chunk_size() -> None:
    """Garante que nenhum chunk exceda o tamanho máximo configurado (1000 caracteres)."""
    texto_longo: str = "palavra" * 500
    chunks: List[str] = split_documents([texto_longo])

    assert len(chunks) > 1
    assert all(len(c) <= 1000 for c in chunks)


def test_split_documents_overlap() -> None:
    """Verifica que a sobreposição faz o final de um chunk aparecer no início do próximo."""
    texto: str = "abcdefghij" * 200
    chunks: List[str] = split_documents([texto], chunk_size=1000, chunk_overlap=200)

    # O final do primeiro chunk deve estar contido no segundo chunk (sobreposição)
    assert chunks[0][-50:] in chunks[1]


def test_split_documents_empty_input() -> None:
    """Garante que a função retorne lista vazia quando não há documentos de entrada."""
    chunks: List[str] = split_documents([])
    assert chunks == []


def test_split_documents_multiple_docs() -> None:
    """Verifica que conteúdos de documentos distintos permanecem nos chunks gerados."""
    doc1: str = "conteúdo do primeiro pdf" * 50
    doc2: str = "conteúdo do segundo pdf" * 50
    chunks: List[str] = split_documents([doc1, doc2])

    assert any("primeiro" in c for c in chunks)
    assert any("segundo" in c for c in chunks)
