# Bug tracker

> This project is for learning new technologies and get some hands-on experience.

## Development

Install Python 3.14 and create the project environment:

```sh
uv python install 3.14
uv sync --dev
```

Starting dev server run:

```sh
uv run uvicorn main:app --reload
```

Output `requirements.txt`:

```sh
uv export --no-dev --format requirements-txt --no-hashes --output-file requirements.txt
```

Create and init db:

```sh
uv run python -m tools.init_db
```

Format, lint, and sort imports with Ruff:

```sh
uv run ruff format .
uv run ruff check --fix .
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
