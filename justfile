# List all available commands
_default:
    @just --list

@install:
    uv sync

# Install dependencies
@bootstrap:
    just install

@clean:
    rm -rf .venv

# Ugrade dependencies
#upgrade:
#    uv run hatch-pip-compile --upgrade --all

# Run sphinx autobuild
@docs-serve:
    uv run --group docs sphinx-autobuild docs docs/_build/html --port 8002

# Run all formatters
@fmt:
    just --fmt --unstable
    uvx ruff format
    uvx pyproject-fmt pyproject.toml
    uvx pre-commit run reorder-python-imports -a

@test:
    uv run pytest --ignore=tests/old

@dj *ARGS:
    cd demo && uv run python manage.py {{ ARGS }}

@check-types:
    uvx mypy --install-types --non-interactive {args:src/falco_app tests}
