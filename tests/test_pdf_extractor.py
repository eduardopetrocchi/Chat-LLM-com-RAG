from unittest.mock import MagicMock, patch

from services.pdf_text_extractor import extract_text_pdf


def _make_fake_page(content: str) -> MagicMock:
    """Cria um objeto fake simulando um langchain_core.documents.Document.

    Args:
        content (str): Texto a ser atribuído ao atributo page_content do objeto fake.

    Returns:
        MagicMock: Objeto simulado com o atributo page_content definido.
    """
    page = MagicMock()
    page.page_content = content
    return page


@patch("services.pdf_text_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_single_page(mock_loader_cls: MagicMock) -> None:
    """Verifica extração correta de texto em um PDF com página única."""
    mock_loader = MagicMock()
    mock_loader.load.return_value = [_make_fake_page("conteúdo da página única")]
    mock_loader_cls.return_value = mock_loader

    resultado: str = extract_text_pdf("fake.pdf")

    assert resultado == "conteúdo da página única"


@patch("services.pdf_text_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_multiple_pages_joined_with_newline(
    mock_loader_cls: MagicMock,
) -> None:
    """Verifica que páginas múltiplas são concatenadas com quebra de linha (\\n)."""
    mock_loader = MagicMock()
    mock_loader.load.return_value = [
        _make_fake_page("página 1"),
        _make_fake_page("página 2"),
        _make_fake_page("página 3"),
    ]
    mock_loader_cls.return_value = mock_loader

    resultado: str = extract_text_pdf("fake.pdf")

    assert resultado == "página 1\npágina 2\npágina 3"


@patch("services.pdf_text_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_empty_document(mock_loader_cls: MagicMock) -> None:
    """Verifica que um PDF sem páginas retorna string vazia."""
    mock_loader = MagicMock()
    mock_loader.load.return_value = []
    mock_loader_cls.return_value = mock_loader

    resultado: str = extract_text_pdf("fake.pdf")

    assert resultado == ""


@patch("services.pdf_text_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_calls_loader_with_correct_path(
    mock_loader_cls: MagicMock,
) -> None:
    """Verifica que o loader é instanciado com o caminho de arquivo exato fornecido."""
    mock_loader = MagicMock()
    mock_loader.load.return_value = [_make_fake_page("conteúdo")]
    mock_loader_cls.return_value = mock_loader

    extract_text_pdf("data/pdfs/aula1.pdf")

    mock_loader_cls.assert_called_once_with("data/pdfs/aula1.pdf")


@patch("services.pdf_text_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_handles_empty_page_content(
    mock_loader_cls: MagicMock,
) -> None:
    """Verifica que páginas com conteúdo vazio geram uma linha em branco na saída."""
    mock_loader = MagicMock()
    mock_loader.load.return_value = [
        _make_fake_page("página 1"),
        _make_fake_page(""),
        _make_fake_page("página 3"),
    ]
    mock_loader_cls.return_value = mock_loader

    resultado: str = extract_text_pdf("fake.pdf")

    assert resultado == "página 1\n\npágina 3"
