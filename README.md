# Bug tracker

> This project is for learning new technologies and get some hands-on experience.

## Development

All commands below are run from the repo root; `--project backend` points `uv` at `backend/pyproject.toml` regardless of your shell's active environment.

Install Python 3.14 and create the project environment:

```sh
uv python install 3.14
uv sync --project backend --dev
```

Starting dev server run:

```sh
uv run --project backend uvicorn backend.main:app --reload
```

Or use the shortcut for your shell:

```sh
make dev        # bash, WSL, macOS/Linux
./dev.ps1       # PowerShell
```

Output `requirements.txt`:

```sh
uv export --project backend --no-dev --format requirements-txt --no-hashes --output-file backend/requirements.txt
```

Create and init db:

```sh
uv run --project backend python -m backend.tools.init_db
```

Format, lint, and sort imports with Ruff:

```sh
uv run --project backend ruff format backend
uv run --project backend ruff check --fix backend
```

[Trello cards](https://trello.com/b/sIgFvLWc/bug-tracker).

## Possible stack

Front end:

- React
- Vue
- GraphQL
- Jest
- D3
- Webpack

Back end:

- Python
  - Flask
  - FastAPI
- Pytest
- uv
- Microservices
- `TODO`: integrate [pydantic](https://pydantic-docs.helpmanual.io/). Data validation library.

DevOps:

- Docker
- Kubernets
- AWS

Database:

- Filesystem
- SQLite
- PostgreSQL
- Redis
- MongoDB or any other key-value

## Plan

### Project structure

- Project
  - Users
  - Projects
    - Issues
      - Comments
