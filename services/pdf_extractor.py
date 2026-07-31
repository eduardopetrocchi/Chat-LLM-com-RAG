"""
Módulo de Extração de PDF (pdf_extractor.py)
--------------------------------------------
Fornece funções utilitárias para ler e extrair texto completo de arquivos PDF.
Usa o PyMuPDF4LLM para uma extração otimizada estruturada em markdown ou texto livre.
"""

from pathlib import Path
from langchain_pymupdf4llm import PyMuPDF4LLMLoader


def extract_text_pdf(file_path: str) -> str:
    """
    Carrega um arquivo PDF e extrai todo o conteúdo de texto de suas páginas.

    Parâmetros:
        file_path (str): Caminho absoluto ou relativo para o arquivo PDF.

    Retorna:
        str: Texto completo extraído e consolidado das páginas do PDF.
    """
    # Inicializa o carregador otimizado PyMuPDF para extração LLM
    loader = PyMuPDF4LLMLoader(file_path)
    
    # Carrega os documentos (uma lista de páginas)
    doc = loader.load()
    
    # Une o texto extraído de cada página com quebras de linha
    content = "\n".join([page.page_content for page in doc])

    return content

