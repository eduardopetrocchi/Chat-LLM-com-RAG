# tests/test_pdf_extractor.py
from unittest.mock import MagicMock, patch

from services.pdf_extractor import extract_text_pdf


def _make_fake_page(content):
    """Cria um objeto fake simulando um langchain_core.documents.Document"""
    page = MagicMock()
    page.page_content = content
    return page


@patch("services.pdf_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_single_page(mock_loader_cls):
    mock_loader = MagicMock()
    mock_loader.load.return_value = [_make_fake_page("conteúdo da página única")]
    mock_loader_cls.return_value = mock_loader

    resultado = extract_text_pdf("fake.pdf")

    assert resultado == "conteúdo da página única"


@patch("services.pdf_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_multiple_pages_joined_with_newline(mock_loader_cls):
    mock_loader = MagicMock()
    mock_loader.load.return_value = [
        _make_fake_page("página 1"),
        _make_fake_page("página 2"),
        _make_fake_page("página 3"),
    ]
    mock_loader_cls.return_value = mock_loader

    resultado = extract_text_pdf("fake.pdf")

    assert resultado == "página 1\npágina 2\npágina 3"


@patch("services.pdf_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_empty_document(mock_loader_cls):
    mock_loader = MagicMock()
    mock_loader.load.return_value = []
    mock_loader_cls.return_value = mock_loader

    resultado = extract_text_pdf("fake.pdf")

    assert resultado == ""


@patch("services.pdf_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_calls_loader_with_correct_path(mock_loader_cls):
    mock_loader = MagicMock()
    mock_loader.load.return_value = [_make_fake_page("conteúdo")]
    mock_loader_cls.return_value = mock_loader

    extract_text_pdf("data/pdfs/aula1.pdf")

    mock_loader_cls.assert_called_once_with("data/pdfs/aula1.pdf")


@patch("services.pdf_extractor.PyMuPDF4LLMLoader")
def test_extract_text_pdf_handles_empty_page_content(mock_loader_cls):
    mock_loader = MagicMock()
    mock_loader.load.return_value = [
        _make_fake_page("página 1"),
        _make_fake_page(""),  # página em branco/sem texto extraível
        _make_fake_page("página 3"),
    ]
    mock_loader_cls.return_value = mock_loader

    resultado = extract_text_pdf("fake.pdf")

    assert resultado == "página 1\n\npágina 3"