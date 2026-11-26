# Physical quantities

## Desarrollo

Requiere [uv](https://docs.astral.sh/uv/). La versión de Python (3.14) está fijada en `.python-version`.

```bash
uv sync                                                   # crea .venv e instala dependencias de desarrollo
uv run python -m unittest discover -s tests -p "test_*.py" # ejecuta los tests
uv run ruff check .                                       # lint
uv run mypy                                               # chequeo de tipos
```

## Estructura

- `src/physical_quantities/`: librería instalable (unidades, dimensiones, cantidades y conversión). API pública en `physical_quantities/__init__.py`.
- `apps/power_budget/`: app de power budget con persistencia SQLite; proyecto uv aparte que depende de la librería.
- `tests/`: tests de la librería. Los tests de la app están en `apps/power_budget/tests/`.

```bash
cd apps/power_budget
uv sync
uv run python -m unittest discover -s tests -p "test_*.py"
```
