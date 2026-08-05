from pathlib import Path
from typing import Union
from langchain_pymupdf4llm import PyMuPDF4LLMLoader


def extract_text_pdf(file_path: Union[str, Path]) -> str:
    """Extrai o texto contínuo de um arquivo PDF utilizando a biblioteca PyMuPDF4LLM.

    Args:
        file_path (Union[str, Path]): Caminho do arquivo PDF a ser processado.

    Returns:
        str: Texto completo extraído das páginas do documento, unidas por quebras de linha.
    """
    loader = PyMuPDF4LLMLoader(str(file_path))
    doc = loader.load()
    content: str = "\n".join([page.page_content for page in doc])

    return content
