# Physical quantities

## Desarrollo

Requiere [uv](https://docs.astral.sh/uv/). La versión de Python (3.14) está fijada en `.python-version`.

```bash
uv sync                                                   # crea .venv e instala dependencias de desarrollo
uv run python -m unittest discover -s tests -p "test_*.py" # ejecuta los tests
uv run ruff check .                                       # lint
uv run mypy                                               # chequeo de tipos
```
