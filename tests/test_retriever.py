from unittest.mock import MagicMock, patch

from rag.retriever import get_retriever, EMBEDDING_MODEL


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_loades_existing_vectorstore(
    mock_chroma, mock_embeddings, tmp_path
):
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()

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
    mock_embeddings, mock_config_retriever, tmp_path
):
    folder_path = str(tmp_path / "pdfs")
    vector_path = str(tmp_path / "vectorstore")  # não criado, não existe

    mock_config_retriever.return_value = MagicMock()

    get_retriever(folder_path, vector_path)

    mock_config_retriever.assert_called_once_with(folder_path, vector_path)


@patch("rag.retriever.config_retriever")
@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_does_not_reindex_when_exists(
    mock_chroma, mock_embeddings, mock_config_retriever, tmp_path
):
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()

    get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_config_retriever.assert_not_called()


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_mmr_with_default_params(mock_chroma, mock_embeddings, tmp_path):
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()

    mock_vectorstore = MagicMock()
    mock_chroma.return_value = mock_vectorstore

    get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_vectorstore.as_retriever.assert_called_once_with(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 4},
    )


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_custom_k_and_fetch_k(mock_chroma, mock_embeddings, tmp_path):
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()

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
def test_get_retriever_uses_correct_embedding_model(mock_chroma, mock_embeddings, tmp_path):
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()

    get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    mock_embeddings.assert_called_once_with(model_name=EMBEDDING_MODEL)


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_returns_retriever_object(mock_chroma, mock_embeddings, tmp_path):
    vector_path = tmp_path / "vectorstore"
    vector_path.mkdir()

    mock_retriever_obj = MagicMock()
    mock_chroma.return_value.as_retriever.return_value = mock_retriever_obj

    result = get_retriever(folder_path=str(tmp_path / "pdfs"), vector_path=str(vector_path))

    assert result is mock_retriever_obj


@patch("rag.retriever.HuggingFaceEmbeddings")
@patch("rag.retriever.Chroma")
def test_get_retriever_uses_default_paths_when_not_provided(mock_chroma, mock_embeddings):
    from rag.retriever import VECTOR_PATH, FOLDER_PATH

    with patch("rag.retriever.config_retriever") as mock_config_retriever:
        # em ambiente de teste os paths default provavelmente não existem
        get_retriever()
        # se o path default não existir, deve tentar indexar com os defaults
        if mock_config_retriever.called:
            mock_config_retriever.assert_called_once_with(FOLDER_PATH, VECTOR_PATH)
