"""
Módulo Localizador de PDFs (pdf_finder.py)
-----------------------------------------
Fornece funções utilitárias para buscar arquivos com extensão PDF em diretórios locais.
"""

from pathlib import Path
from typing import List


def find_pdfs(dir_path: str) -> List[Path]:
    """
    Busca e lista todos os arquivos com extensão .pdf localizados no diretório fornecido.

    Parâmetros:
        dir_path (str): Caminho do diretório a ser pesquisado.

    Retorna:
        List[Path]: Lista contendo caminhos do tipo Path para os arquivos PDF encontrados.
    """
    # Usa glob para listar todos os arquivos terminando em .pdf no diretório
    return list(Path(dir_path).glob("*.pdf"))

