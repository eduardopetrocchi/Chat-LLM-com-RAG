"""
Módulo do Agente de Chat (chat_agent.py)
--------------------------------------
Define a lógica de conversação do assistente. Gerencia o histórico de conversas,
enviando as mensagens anteriores e a nova pergunta para a chain do RAG.
"""

from typing import Tuple, List
from langchain_core.messages import AIMessage, HumanMessage


def chat_llm(rag_chain, user_input: str, chat_history: List) -> Tuple[str, List]:
    """
    Processa a pergunta do usuário utilizando a chain do RAG,
    gerencia e atualiza o histórico da conversação.

    Parâmetros:
        rag_chain: Chain do LangChain configurada com retriever e LLM.
        user_input (str): Pergunta ou entrada atual do usuário.
        chat_history (List): Lista contendo o histórico de mensagens (Human/AI).

    Retorna:
        Tuple[str, List]: Resposta do assistente e o histórico de chat atualizado.
    """
    # Adiciona a nova mensagem do usuário ao histórico de chat
    chat_history.append(HumanMessage(content=user_input))

    # Invoca a chain do RAG passando a pergunta atual e o histórico completo
    response = rag_chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    
    # Extrai o texto da resposta gerada
    res = response.get("answer", "")

    # Adiciona a resposta do assistente ao histórico de chat
    chat_history.append(AIMessage(content=res))

    return res, chat_history