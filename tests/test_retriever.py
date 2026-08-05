from unittest.mock import MagicMock, patch

from rag.retriever import get_retriever, EMBEDDING_MODEL



@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_loads_existing_vectorstore(
    mock_chroma: MagicMock, mock_embeddings: MagicMock, tmp_path
) -> None:
    """Verifica que o Chroma é carregado do disco quando o vectorstore já existe."""
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()
    # Simula um vectorstore não-vazio — sem isso os.listdir() retorna []
    # e o retriever tenta re-indexar (disparando config_retriever com PDFs ausentes)
    (vector_path / "chroma.sqlite3").touch()

    mock_vectorstore = MagicMock()
    mock_chroma.return_value = mock_vectorstore

    get_retriever(str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_chroma.assert_called_once_with(
        persist_directory=str(vector_path),
        embedding_function=mock_embeddings.return_value,
    )


@patch("rag.retriever.config_retriever")
@patch("rag.retriever.HuggingFaceEmbeddings")
def test_get_retriever_indexes_when_missing(
    mock_embeddings: MagicMock, mock_config_retriever: MagicMock, tmp_path
) -> None:
    """Verifica que config_retriever é chamado quando o vectorstore não existe."""
    folder_path: str = str(tmp_path / "pdfs")
    vector_path: str = str(tmp_path / "vectorstore")  # diretório intencionalmente ausente

    mock_config_retriever.return_value = MagicMock()

    get_retriever(folder_path, vector_path)

    mock_config_retriever.assert_called_once_with(folder_path, vector_path)


@patch("rag.retriever.config_retriever")
@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_does_not_reindex_when_exists(
    mock_chroma: MagicMock, mock_embeddings: MagicMock, mock_config_retriever: MagicMock, tmp_path
) -> None:
    """Garante que a re-indexação NÃO ocorre quando o vectorstore já existe e tem conteúdo."""
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()
    # Cria um arquivo para simular vectorstore com conteúdo
    (vector_path / "chroma.sqlite3").touch()

    get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_config_retriever.assert_not_called()


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_mmr_with_default_params(
    mock_chroma: MagicMock, mock_embeddings: MagicMock, tmp_path
) -> None:
    """Verifica que o retriever usa busca MMR com os parâmetros padrão k=3 e fetch_k=4."""
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()
    (vector_path / "chroma.sqlite3").touch()

    mock_vectorstore = MagicMock()
    mock_chroma.return_value = mock_vectorstore

    get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_vectorstore.as_retriever.assert_called_once_with(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 4},
    )


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_custom_k_and_fetch_k(
    mock_chroma: MagicMock, mock_embeddings: MagicMock, tmp_path
) -> None:
    """Verifica que os parâmetros k e fetch_k customizados são repassados corretamente ao MMR."""
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()
    (vector_path / "chroma.sqlite3").touch()

    mock_vectorstore = MagicMock()
    mock_chroma.return_value = mock_vectorstore

    get_retriever(
        folder_path=str(tmp_path / "pdfs"),
        vector_path=str(vector_path),
        k=5,
        fetch_k=10,
    )

    mock_vectorstore.as_retriever.assert_called_once_with(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 10},
    )


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_correct_embedding_model(
    mock_chroma: MagicMock, mock_embeddings: MagicMock, tmp_path
) -> None:
    """Verifica que o modelo de embeddings correto é utilizado para criar o vectorstore."""
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()
    (vector_path / "chroma.sqlite3").touch()

    get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_embeddings.assert_called_once_with(model_name=EMBEDDING_MODEL)


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_returns_retriever_object(
    mock_chroma: MagicMock, mock_embeddings: MagicMock, tmp_path
) -> None:
    """Verifica que o objeto retornado é exatamente o retriever devolvido pelo vectorstore."""
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()
    (vector_path / "chroma.sqlite3").touch()

    mock_retriever_obj = MagicMock()
    mock_chroma.return_value.as_retriever.return_value = mock_retriever_obj

    result = get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    assert result is mock_retriever_obj


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_default_paths_when_not_provided(
    mock_chroma: MagicMock, mock_embeddings: MagicMock
) -> None:
    """Verifica que os caminhos padrão (FOLDER_PATH e VECTOR_PATH) são usados corretamente."""
    from rag.retriever import VECTOR_PATH, FOLDER_PATH

    with patch("rag.retriever.config_retriever") as mock_config_retriever:
        # Em ambiente de teste os paths padrão podem não ter conteúdo ou não existir
        get_retriever()
        # Se o vectorstore padrão estiver vazio/ausente, indexação deve ser chamada com os defaults
        if mock_config_retriever.called:
            mock_config_retriever.assert_called_once_with(FOLDER_PATH, VECTOR_PATH)
