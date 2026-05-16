# We Remember

Privacy-first, self-hostable calendar. No trackers, no Google — your data stays
local.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.13

## Getting started

1. Clone the repository and enter the project directory:

   ```sh
   git clone https://github.com/OranguStudio/we-remember.git
   cd we-remember
   ```

2. Install dependencies:

   ```sh
   uv sync
   ```

3. Configure environment:

   ```sh
   cp .env.example .env
   ```

The Django code reads configuration from environment variables with
`os.environ`. It does not load `.env` files directly.

## Development

Run the Django development server:

```sh
export DJANGO_SECRET_KEY=dev-secret-key
uv run python manage.py runserver
```

Run linting:

```sh
uv run ruff check .
```

Run tests:

```sh
uv run pytest
```
