from langchain_core.tools import BaseTool
from langchain_core.tools.retriever import create_retriever_tool

from rag.retriever import get_retriever


def recovery_tool() -> BaseTool:
    """Cria e retorna a ferramenta de recuperação (retriever tool) para o agente.

    Esta ferramenta permite ao agente consultar documentos pedagógicos e diretrizes da BNCC
    armazenados na base de vetores Chroma.

    Returns:
        BaseTool: Ferramenta configurada do LangChain pronta para ser consumida por agentes.
    """
    retriever = get_retriever()
    retriever_tool: BaseTool = create_retriever_tool(
        retriever,
        "retriever_docs",
        "Consulte esta ferramenta para buscar conteúdos pedagógicos oficiais, "
        "diretrizes da BNCC, planos de aula e exercícios de referência em PDFs educacionais. "
        "Sempre use esta busca ao elaborar o material didático para garantir fundamentação teórica.",
    )

    return retriever_tool
