from unittest.mock import MagicMock
from langchain_core.messages import AIMessage, HumanMessage

from agents.chat_agent import chat_llm


def test_chat_agent_uses_history():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "resposta simulada"}

    historico = []
    resposta, novo_historico = chat_llm(
        mock_chain, "Qual a capital da França?", historico
    )

    assert isinstance(novo_historico[0], HumanMessage)
    assert novo_historico[0].content == "Qual a capital da França?"


def test_chat_llm_append_ai_message():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "A capital é Paris."}

    resposta, novo_historico = chat_llm(mock_chain, "Qual a capital da França?", [])

    assert isinstance(novo_historico[-1], AIMessage)
    assert novo_historico[-1].content == "A capital é Paris."


def test_chat_llm_return_answer_string():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "resposta esperada"}

    resposta, _ = chat_llm(mock_chain, "qualquer pergunta", [])

    assert resposta == "resposta esperada"


def test_chat_llm_calls_with_correct_args():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "ok"}

    historico_inicial = [
        HumanMessage(content="Usuário: Oi!"),
        AIMessage(content="IA: Olá!"),
    ]
    chat_llm(mock_chain, "nova_pergunta", historico_inicial)

    args, kwargs = mock_chain.invoke.call_args
    chamada = args[0]

    assert chamada["input"] == "nova_pergunta"
    # o chat_history passado pro invoke já deve incluir a nova HumanMessage
    assert chamada["chat_history"][-1].content == "nova_pergunta"


def test_chat_llm_history_grows_by_two():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "resposta"}

    historico = []
    _, novo_historico = chat_llm(mock_chain, "pergunta 1", historico)

    assert len(novo_historico) == 2  # (1human 1AI)


def test_chat_llm_accumulates_history_across_calls():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "resposta"}

    historico = []
    _, historico = chat_llm(mock_chain, "pergunta 1", historico)
    _, historico = chat_llm(mock_chain, "pergunta 2", historico)

    assert len(historico) == 4  # (2human 2AI)
    assert historico[0].content == "pergunta 1"
    assert historico[2].content == "pergunta 2"


def test_chat_llm_does_not_mutate_original_history():
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"answer": "resposta"}

    historico_original = [HumanMessage(content="mensagem antiga")]
    _, novo_historico = chat_llm(mock_chain, "pergunta nova", historico_original)

    assert len(historico_original) == 1  # não deve ter mudado
