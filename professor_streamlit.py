import os
from datetime import datetime
from typing import Any, Dict

import pypandoc
import streamlit as st

from agente.agente_assistente import assistente_agent
from services.prompt_selector import materia_prompt

# Configuração da página
st.set_page_config(page_title="Assistente de professores", layout="centered")
st.title("Assistente de professores")

# Inicialização do estado da sessão Streamlit
if "objetivo" not in st.session_state:
    st.session_state["objetivo"] = None

if "doc_content" not in st.session_state:
    st.session_state["doc_content"] = ""

# Dados de domínio: matérias e seus tópicos disponíveis
TOPICO_POR_MATERIA: Dict[str, list] = {
    "Matemática": ["Soma", "Subtração", "Multiplicação", "Divisão"],
    "Português": ["Alfabetização", "Letramento", "Ortografia", "Gêneros"],
    "Ciências da Natureza": ["Ecossistemas", "Corpo", "Matéria", "Universo"],
    "Informática": ["Cidadania", "Programação", "Pesquisa", "Hardware"],
    "Ed. Física": ["Esportes", "Jogos", "Corpo", "Dança"],
}

# Seleção da matéria fora do formulário para atualizar dinamicamente os tópicos
materia: str = st.selectbox("Matéria", list(TOPICO_POR_MATERIA.keys()))

# Formulário principal de entrada de dados
with st.form("formulario"):
    serie: str = st.selectbox("Série", ["1ª", "2ª", "3ª", "4ª"])
    topico: str = st.selectbox("Tópico", TOPICO_POR_MATERIA[materia])
    objetivo: str = st.selectbox(
        "Objetivo", ["Plano de aula", "Lista de exercícios", "Provas"]
    )
    assunto: str = st.text_input(
        "Assunto",
        placeholder="Desenhos, filmes, passeios, etc.",
    )
    questoes: str = st.text_input(
        "Quantidade de questões",
        placeholder="Questões para avaliações e listas de exercícios",
        value="5",
    )
    gerar_documento: bool = st.form_submit_button("Gerar documento")

# Processamento após submissão do formulário
if gerar_documento:
    # Seleciona o template de prompt específico para a matéria
    MATERIA_PROMPT: str = materia_prompt(materia)
    prompt: str = MATERIA_PROMPT.format(
        serie=serie,
        topico=topico,
        objetivo=objetivo,
        assunto=assunto,
        questoes=questoes,
    )

    # Executa o agente e aguarda a resposta
    with st.spinner("Executando os agentes, aguarde..."):
        resposta: Dict[str, Any] = assistente_agent(prompt)

    # Mapeia o objetivo para o nome do arquivo/pasta de saída
    nome: str = {
        "Lista de exercícios": "lista_exercicios",
        "Provas": "prova",
    }.get(objetivo, "plano_aula")

    # Cria os diretórios de saída se não existirem
    pasta: str = f"resultados/{nome}"
    os.makedirs("resultados", exist_ok=True)
    os.makedirs(pasta, exist_ok=True)

    # Gera nome do arquivo com timestamp para evitar sobrescritas
    nome_arquivo: str = f"{nome}-{datetime.now().strftime('%d%m%Y-%H%M%S')}.docx"
    caminho: str = f"{pasta}/{nome_arquivo}"

    # Converte o Markdown retornado pelo agente para o formato .docx
    conteudo_md: str = resposta["messages"][-1].content
    pypandoc.convert_text(conteudo_md, to="docx", format="md", outputfile=caminho)

    st.success(f"Arquivo salvo em {caminho}")

    # Exibe o conteúdo gerado na interface
    st.markdown(conteudo_md)
