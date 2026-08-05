from typing import Any, Dict
from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

from tools.recovery_tool import recovery_tool
from models.model_loader import get_model

# Inicialização do modelo LLM padrão (Groq) e das ferramentas do agente
llm: BaseChatModel = get_model()
retriever_tool: BaseTool = recovery_tool()
tools_list: list[BaseTool] = [retriever_tool]


def assistente_agent(prompt: str) -> Dict[str, Any]:
    """Cria e executa o agente assistente pedagógico para responder à solicitação do professor.

    Args:
        prompt (str): Texto contendo as instruções e contexto formatados para a geração do documento.

    Returns:
        Dict[str, Any]: Dicionário contendo as mensagens retornadas pela execução do agente,
                       onde a última mensagem contém a resposta em Markdown.
    """
    agent = create_agent(llm, tools=tools_list)
    resposta: Dict[str, Any] = agent.invoke({"messages": [("user", prompt)]})
    return resposta



