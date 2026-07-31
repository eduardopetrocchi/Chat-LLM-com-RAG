"""
Módulo de Configuração da Chain RAG (config.py)
-----------------------------------------------
Configura o fluxo de recuperação de documentos (RAG) considerando o histórico
da conversação (History-Aware Retriever). Combina o LLM com o retriever de vetores
para gerar respostas contextualizadas.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from rag.prompts import CONTEXT_Q_SYSTEM_PROMPT, SYSTEM_PROMPT


def config_rag_chain(llm, retriever):
    """
    Configura e retorna a chain RAG final, unindo recuperação de contexto
    sensível ao histórico de chat e geração de resposta.

    Parâmetros:
        llm: Instância do modelo de linguagem configurado.
        retriever: Retriever do banco de vetores (ChromaDB).

    Retorna:
        Chain RAG pronta para receber entradas do usuário e responder com contexto.
    """
    # 1. Prompt para reformular a pergunta do usuário caso haja histórico
    # Isso garante que perguntas que referenciem mensagens anteriores (ex: "e ele?") sejam resolvidas
    context_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CONTEXT_Q_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "Question: {input}"),
        ]
    )

    # Cria o retriever ciente do histórico
    history_aware_retriever = create_history_aware_retriever(
        llm=llm, retriever=retriever, prompt=context_q_prompt
    )

    # 2. Prompt para resposta final, integrando o contexto recuperado
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "Pergunta: {input}\n\nContexto: {context}"),
        ]
    )

    # Cria a chain para combinar/inserir os documentos (stuffing) no prompt
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # 3. Cria a chain RAG combinando a recuperação de documentos e a resposta final
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return rag_chain

