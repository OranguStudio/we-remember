# We Remember

Privacy-first, self-hostable calendar. No trackers, no Google — your data stays
local.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.13
- Docker with the Docker Compose plugin, or
- Podman with Podman Compose

Podman is preferred for local self-hosting experiments because it runs
rootless by default.

## Getting started

### Local setup

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

4. Load environment variables into the current terminal session:

   ```sh
   set -a && source .env && set +a
   ```

   This injects the `.env` values into the current terminal session for
   development commands.

The Django code reads configuration from environment variables with
`os.environ`. It does not load `.env` files directly.

### Containerized setup

1. Clone the repository and enter the project directory:

   ```sh
   git clone https://github.com/OranguStudio/we-remember.git
   cd we-remember
   ```

2. Configure environment:

   ```sh
   cp .env.example .env
   ```

   Docker Compose reads `.env` through `env_file`, so container startup does
   not require sourcing the file in your shell.

3. Edit `.env` and set at least:

   - `DJANGO_SECRET_KEY`
   - `DJANGO_ALLOWED_HOSTS`

4. Start the application with Docker Compose:

   ```sh
   docker compose up --build
   ```

   Or with Podman Compose:

   ```sh
   podman compose up --build
   ```

The application listens on <http://localhost:8000>. The health check endpoint
is available at <http://localhost:8000/healthz/>.

Stop the application:

```sh
docker compose down
```

Or with Podman Compose:

```sh
podman compose down
```

SQLite data is stored in the named `sqlite_data` volume and persists across
`docker compose down` or `podman compose down`. Use `down -v` only when you
want to delete the local SQLite data volume too.

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
