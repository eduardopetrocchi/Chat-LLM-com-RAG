"""
Módulo de Ingestão de Documentos (ingest.py)
--------------------------------------------
Varre uma pasta local em busca de arquivos PDF, extrai seus conteúdos textuais,
divide o texto em fragmentos (chunks) e os insere em um banco de vetores ChromaDB
utilizando embeddings do HuggingFace.

Este módulo é executado de forma automática por `retriever.py` se nenhum banco de
vetores for encontrado no caminho especificado durante a inicialização do chat.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from services.pdf_extractor import extract_text_pdf
from services.pdf_finder import find_pdfs

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"


def config_retriever(folder_path: str, vector_path: str) -> Chroma:
    """
    Realiza o pipeline completo de RAG Ingest:
    1. Busca todos os PDFs no diretório especificado.
    2. Extrai o texto contido em cada documento PDF.
    3. Segmenta o texto em partes menores (chunks) para melhor indexação.
    4. Inicializa o modelo de embeddings do HuggingFace.
    5. Salva os embeddings e o texto no banco de vetores ChromaDB.

    Parâmetros:
        folder_path (str): Diretório onde estão os PDFs originais.
        vector_path (str): Diretório para persistir os índices do ChromaDB.

    Retorna:
        Chroma: Objeto do banco de dados vetorial inicializado e populado.
    """
    # Localiza arquivos PDF no diretório
    pdf_files = find_pdfs(folder_path)
    if not pdf_files:
        print(f"Aviso: Nenhum arquivo PDF encontrado em {folder_path}")
        return None

    # Extrai o texto de todos os arquivos encontrados
    loaded_documents = [extract_text_pdf(str(pdf)) for pdf in pdf_files]

    # Configura o divisor de texto (Text Splitter)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    # Divide o texto carregado em fragmentos menores (chunks)
    chunks = []
    for doc in loaded_documents:
        chunks.extend(text_splitter.split_text(doc))

    # Inicializa o modelo de geração de representação vetorial
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Cria e persiste o banco de vetores com os fragmentos e seus embeddings
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=vector_path,
    )

    print("Documentos vetorados com sucesso e salvos no ChromaDB!")
    return vectorstore
