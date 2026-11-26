import json
from os import PathLike
from typing import Any

type StrPath = str | PathLike[str]


def json_to_dict(json_file: StrPath, encoding: str = "utf-8") -> dict[str, Any]:
    """Load a JSON file into a dict.

    Args:
        json_file: Path to the JSON file.
        encoding: Encoding of the file. Defaults to 'utf-8'.

    Returns:
        Dictionary with the JSON content of the file.
    """
    with open(json_file, encoding=encoding) as file:
        return json.load(file)


def json_string_to_dict(json_string: str) -> dict[str, Any]:
    return json.loads(json_string)


def dict_to_json(
    data: dict[str, Any], json_file: StrPath, ensure_ascii: bool = False, encoding: str = "utf-8"
) -> None:
    with open(json_file, "w", encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=ensure_ascii)


def dict_to_json_string(data: dict[str, Any], ensure_ascii: bool = False) -> str:
    return json.dumps(data, ensure_ascii=ensure_ascii)
