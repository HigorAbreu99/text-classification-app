import json
from pathlib import Path
from typing import Any, Dict, List, Union, Optional


def read_json(
    file_path: Union[str, Path],
) -> Optional[Union[Dict[str, Any], List[Any]]]:
    """
    Lê um arquivo JSON e o carrega em um dicionário ou lista Python.

    Args:
        file_path (Union[str, Path]): O caminho para o arquivo JSON.

    Returns:
        Optional[Union[Dict[str, Any], List[Any]]]: O conteúdo do JSON como um objeto Python
        (dicionário ou lista), ou None se ocorrer um erro.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado em '{file_path}'")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo em '{file_path}' não contém um JSON válido.")
        return None


def write_json(
    data: Union[Dict[str, Any], List[Any]], file_path: Union[str, Path]
) -> None:
    """
    Escreve um dicionário ou lista Python em um arquivo JSON.

    Args:
        data (Union[Dict[str, Any], List[Any]]): O objeto Python a ser salvo.
        file_path (Union[str, Path]): O caminho do arquivo onde o JSON será salvo.
                                      Os diretórios pais serão criados se não existirem.
    """
    try:
        # Garante que o diretório pai do arquivo exista
        path_obj = Path(file_path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(path_obj, "w", encoding="utf-8") as f:
            # indent=2: Formata o JSON para ser legível por humanos
            # ensure_ascii=False: Garante que caracteres como 'ç' e 'ã' sejam salvos corretamente
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Dados salvos com sucesso em '{file_path}'")

    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo em '{file_path}': {e}")
