"""Caminhos padrão do projeto, relativos à raiz do repositório."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDFS_DIR = PROJECT_ROOT / "data" / "pdfs"
VECTORSTORE_DIR = PROJECT_ROOT / "data" / "vectorstore" / "index_chromaDB_professores"
