from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from services.prompt_selector import materia_prompt

# Fixtures
@pytest.fixture
def prompt_matematica() -> str:
    """Retorna um prompt formatado de Matemática para uso nos testes."""
    template: str = materia_prompt("Matemática")
    return template.format(
        serie="1ª",
        topico="Soma",
        objetivo="Lista de exercícios",
        assunto="Animais",
        questoes="3",
    )


# Testes unitários com mock (sem chamada real ao LLM)
@patch("agente.agente_assistente.create_agent")
def test_assistente_agent_retorna_dict(mock_create_agent: MagicMock) -> None:
    """Verifica que assistente_agent retorna um dicionário com a chave 'messages'."""
    from agente.agente_assistente import assistente_agent

    # Configura o agente mock para retornar uma resposta simulada
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {
        "messages": [MagicMock(content="Resposta pedagógica gerada pelo agente.")]
    }
    mock_create_agent.return_value = mock_agent

    resposta: Dict[str, Any] = assistente_agent(
        "Crie um plano de aula sobre soma para 1ª série."
    )

    assert isinstance(resposta, dict)
    assert "messages" in resposta


@patch("agente.agente_assistente.create_agent")
def test_assistente_agent_conteudo_nao_vazio(mock_create_agent: MagicMock) -> None:
    """Verifica que o conteúdo da última mensagem do agente não está vazio."""
    from agente.agente_assistente import assistente_agent

    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {
        "messages": [MagicMock(content="# Plano de Aula\n\nObjetivos: ...")]
    }
    mock_create_agent.return_value = mock_agent

    resposta: Dict[str, Any] = assistente_agent("Crie um plano de aula.")
    conteudo: str = resposta["messages"][-1].content

    assert len(conteudo) > 0


@patch("agente.agente_assistente.create_agent")
def test_assistente_agent_chama_invoke_com_prompt(mock_create_agent: MagicMock) -> None:
    """Verifica que o agente é invocado com o prompt formatado como mensagem de usuário."""
    from agente.agente_assistente import assistente_agent

    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {"messages": [MagicMock(content="ok")]}
    mock_create_agent.return_value = mock_agent

    prompt: str = "Crie uma prova de matemática."
    assistente_agent(prompt)

    mock_agent.invoke.assert_called_once_with({"messages": [("user", prompt)]})


# Testes de integração: ferramenta RAG e prompt_selector
def test_materia_prompt_retorna_string_nao_vazia() -> None:
    """Verifica que materia_prompt retorna um template de string não vazio para todas as matérias."""
    materias: List[str] = [
        "Matemática",
        "Português",
        "Ciências da Natureza",
        "Informática",
        "Ed. Física",
    ]
    for materia in materias:
        template: str = materia_prompt(materia)
        assert isinstance(template, str)
        assert len(template) > 0, f"Template vazio para matéria: {materia}"


def test_materia_prompt_contem_placeholders(prompt_matematica: str) -> None:
    """Verifica que o prompt formatado substitui corretamente todos os placeholders."""
    # Após formatação, nenhum placeholder deve permanecer no texto
    assert "{serie}" not in prompt_matematica
    assert "{topico}" not in prompt_matematica
    assert "{objetivo}" not in prompt_matematica
    assert "{assunto}" not in prompt_matematica
    assert "{questoes}" not in prompt_matematica


def test_materia_prompt_materia_invalida() -> None:
    """Verifica que materia_prompt lança ValueError para matéria não cadastrada."""
    with pytest.raises(ValueError, match="inválida"):
        materia_prompt("Filosofia")


def test_materia_prompt_menciona_retriever_docs() -> None:
    """Verifica que todos os prompts orientam o agente a consultar a ferramenta retriever_docs."""
    materias: List[str] = [
        "Matemática",
        "Português",
        "Ciências da Natureza",
        "Informática",
        "Ed. Física",
    ]
    for materia in materias:
        template: str = materia_prompt(materia)
        assert (
            "retriever_docs" in template
        ), f"O prompt de '{materia}' não menciona a ferramenta 'retriever_docs'."


@patch("tools.recovery_tool.get_retriever")
def test_recovery_tool_cria_ferramenta(mock_get_retriever: MagicMock) -> None:
    """Verifica que recovery_tool cria corretamente a ferramenta de recuperação RAG."""
    from tools.recovery_tool import recovery_tool

    mock_retriever = MagicMock()
    mock_get_retriever.return_value = mock_retriever

    tool = recovery_tool()

    assert tool is not None
    assert tool.name == "retriever_docs"
