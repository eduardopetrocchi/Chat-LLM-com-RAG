import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
MISTRAL_API_KEY: str | None = os.getenv("MISTRAL_API_KEY")


def load_groq(id_model: str = "llama-3.3-70b-versatile") -> ChatGroq:
    """Inicializa e retorna uma instância do modelo ChatGroq.

    Args:
        id_model (str): Identificador do modelo no Groq. Padrão 'llama-3.3-70b-versatile'.

    Returns:
        ChatGroq: Instância configurada do modelo LLM Groq.
    """
    return ChatGroq(
        model=id_model,
        temperature=0.2,
        max_tokens=3000,
        max_retries=2,
        api_key=GROQ_API_KEY,
    )


def load_mistral(id_model: str = "mistral-medium-latest") -> ChatMistralAI:
    """Inicializa e retorna uma instância do modelo ChatMistralAI.

    Args:
        id_model (str): Identificador do modelo no Mistral AI. Padrão 'mistral-medium-latest'.

    Returns:
        ChatMistralAI: Instância configurada do modelo LLM Mistral.
    """
    return ChatMistralAI(
        model_name=id_model,
        temperature=0.2,
        max_tokens=3000,
        max_retries=2,
        api_key=MISTRAL_API_KEY,
    )


def get_model(model: str = "groq") -> BaseChatModel:
    """Carrega o modelo de linguagem (LLM) especificado.

    Args:
        model (str): Nome do provedor do modelo ('groq' ou 'mistral'). Padrão 'groq'.

    Returns:
        BaseChatModel: Objeto LLM correspondente.

    Raises:
        ValueError: Se o modelo solicitado não for suportado.
    """
    if model == "groq":
        return load_groq()
    if model == "mistral":
        return load_mistral()

    raise ValueError(
        f"Modelo '{model}' não suportado. Escolha entre 'groq' ou 'mistral'."
    )
