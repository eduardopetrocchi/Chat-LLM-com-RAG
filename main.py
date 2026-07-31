"""
Módulo Principal (main.py)
--------------------------
Ponto de entrada do assistente virtual de RAG (Retrieval-Augmented Generation).
Inicializa o LLM, carrega o banco de vetores ChromaDB, configura a chain de RAG
e executa um loop de interação via terminal (CLI) com o usuário.
"""

from agents.chat_agent import chat_llm
from models.model_loader import get_model
from rag.paths import VECTORSTORE_DIR
from rag.retriever import get_retriever
from rag.config import config_rag_chain


def main() -> None:
    """
    Função principal que gerencia o fluxo de execução do assistente:
    1. Carrega o modelo de linguagem (LLM).
    2. Inicializa o retriever com base no banco de vetores persistido.
    3. Configura a chain do RAG (com histórico e recuperação).
    4. Inicia o loop de interação interativa com o usuário.
    """
    print("Carregando o modelo e índice de documentos...")

    # Inicialização dos componentes do RAG
    llm = get_model()
    retriever = get_retriever(str(VECTORSTORE_DIR))
    rag_chain = config_rag_chain(llm, retriever)

    # Mantém o histórico de mensagens da conversa atual
    chat_history = []

    print("Assistente pronto. Digite 'sair', 'exit' ou 'quit' para encerrar.\n")

    # Loop principal do chat interativo
    while True:
        try:
            # Captura a entrada do usuário
            user_input = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            # Trata interrupções amigavelmente (ex: Ctrl+C ou Ctrl+D)
            print("\nEncerrando o assistente.")
            break

        # Ignora entradas vazias
        if not user_input:
            continue

        # Verifica se o usuário deseja sair
        if user_input.lower() in ("sair", "exit", "quit"):
            print("\nEncerrando o assistente.")
            break

        try:
            # Invoca o agente de chat enviando a pergunta, a chain e o histórico
            resposta, chat_history = chat_llm(rag_chain, user_input, chat_history)
        except Exception as e:
            # Exibe erros ocorridos durante a inferência sem derrubar o loop
            print(f"Erro ao processar a pergunta: {e}")
            continue

        # Exibe a resposta do assistente no terminal
        print(f"Assistente: {resposta}\n")


if __name__ == "__main__":
    main()
