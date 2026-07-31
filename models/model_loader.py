"""
Módulo de Carregamento de Modelos (model_loader.py)
--------------------------------------------------
Responsável por instanciar os clientes de LLM suportados pelo projeto (Groq, Mistral).
Lê as credenciais necessárias das variáveis de ambiente usando o python-dotenv.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def load_groq() -> ChatGroq:
    """
    Instancia o modelo Llama da Groq Cloud.

    Retorna:
        ChatGroq: Instância do LLM da Groq.
    """
    if not GROQ_API_KEY:
        raise ValueError("A variável de ambiente GROQ_API_KEY não foi configurada.")

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=3000,
        max_retries=2,
        api_key=GROQ_API_KEY,
    )


def load_mistral() -> ChatMistralAI:
    """
    Instancia o modelo Mistral Medium da Mistral AI.

    Retorna:
        ChatMistralAI: Instância do LLM da Mistral.
    """
    if not MISTRAL_API_KEY:
        raise ValueError("A variável de ambiente MISTRAL_API_KEY não foi configurada.")

    return ChatMistralAI(
        model_name="mistral-medium-3-5",
        temperature=0.2,
        max_tokens=3000,
        max_retries=2,
        api_key=MISTRAL_API_KEY,
    )


def get_model(model: str = "groq"):
    """
    Função fábrica que retorna o LLM correspondente ao nome solicitado.

    Parâmetros:
        model (str): Nome do provedor do modelo ("groq" ou "mistral"). Default: "groq".

    Retorna:
        Um objeto LLM compatível com LangChain (ChatGroq ou ChatMistralAI).

    Exceções:
        ValueError: Caso o modelo solicitado não seja suportado ou a API key não esteja configurada.
    """
    model_lower = model.lower()

    if model_lower == "groq":
        return load_groq()
    if model_lower == "mistral":
        return load_mistral()

    raise ValueError(f"Modelo '{model}' não é suportado. Escolha entre: groq, mistral.")
