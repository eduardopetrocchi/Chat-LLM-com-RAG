from pathlib import Path
from typing import List, Union


def find_pdfs(dir_path: Union[str, Path]) -> List[Path]:
    """Busca e lista todos os arquivos com extensão .pdf presentes em um diretório.

    Args:
        dir_path (Union[str, Path]): Caminho do diretório para a busca de arquivos.

    Returns:
        List[Path]: Lista de objetos Path representando os caminhos de todos os arquivos PDF encontrados.
    """
    return list(Path(dir_path).glob("*.pdf"))
