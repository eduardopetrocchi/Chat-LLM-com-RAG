from typing import Dict
from prompts.ciencias_prompt import CIENCIAS_PROMPT
from prompts.ed_fisica_prompt import EDUCACAO_FISICA_PROMPT
from prompts.informatica_prompt import INFORMATICA_PROMPT
from prompts.matematica_prompt import MATEMATICA_PROMPT
from prompts.portugues_prompt import PORTUGUES_PROMPT

# Mapeamento centralizado de matérias para os respectivos prompts do sistema
PROMPT_MAP: Dict[str, str] = {
    "Matemática": MATEMATICA_PROMPT,
    "Português": PORTUGUES_PROMPT,
    "Ciências da Natureza": CIENCIAS_PROMPT,
    "Informática": INFORMATICA_PROMPT,
    "Ed. Física": EDUCACAO_FISICA_PROMPT,
}


def materia_prompt(materia: str) -> str:
    """Retorna o template de prompt específico para a matéria selecionada.

    Args:
        materia (str): Nome da disciplina (ex: 'Matemática', 'Português', etc.).

    Returns:
        str: Template do prompt pedagógico correspondente.

    Raises:
        ValueError: Caso a matéria informada não esteja cadastrada no sistema.
    """
    if materia not in PROMPT_MAP:
        raise ValueError(
            f"Matéria '{materia}' inválida. Matérias suportadas: {list(PROMPT_MAP.keys())}"
        )

    return PROMPT_MAP[materia]
