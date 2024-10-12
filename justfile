# List all available commands
_default:
    @just --list

@install:
    hatch run python --version

# Install dependencies
@bootstrap:
    hatch env create

@clean:
    hatch env prune

# Ugrade dependencies
upgrade:
    hatch run hatch-pip-compile --upgrade --all

# Run all formatters
@fmt:
    just --fmt --unstable
    hatch fmt --formatter
    hatch run pyproject-fmt pyproject.toml
    hatch run pre-commit run reorder-python-imports -a

@test:
    hatch run pytest --ignore=tests/old

@dj *ARGS:
    cd demo && hatch run python manage.py {{ ARGS }}
