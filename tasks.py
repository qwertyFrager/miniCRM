# tasks.py
from invoke import task

COMPOSE_FILE = "docker-compose.yml"
ENV_FILE = ".env"
SERVICE = "api"

COMPOSE = f"docker compose -f {COMPOSE_FILE} --env-file {ENV_FILE}"


@task
def help(c):
    print("Available commands:")
    print("  uv run invoke docker-build        # собрать образ и запустить")
    print("  uv run invoke docker-up           # поднять в фоне")
    print("  uv run invoke docker-down         # остановить")
    print("  uv run invoke docker-down-v       # остановить и удалить volumes")
    print("  uv run invoke logs                # логи api")
    print("  uv run invoke ps                  # статус контейнеров")
    print("  uv run invoke db-revision -m MSG  # создать миграцию Alembic")
    print("  uv run invoke db-up               # применить миграции")
    print("  uv run invoke db-down             # откатить на один шаг")
    print("  uv run invoke db-history          # история миграций")
    print("  uv run invoke db-current          # текущая ревизия")
    print("  uv run invoke tests               # запустить pytest")


# ===== Docker =====
@task
def docker_build(c):
    """Собрать образ и запустить в foreground (для отладки логов)."""
    c.run(f"{COMPOSE} up --build")

@task
def docker_up(c):
    """Поднять контейнеры в фоне."""
    c.run(f"{COMPOSE} up -d")

@task
def docker_down(c):
    """Остановить контейнеры."""
    c.run(f"{COMPOSE} down")

@task
def docker_down_v(c):
    """Остановить контейнеры и удалить volumes."""
    c.run(f"{COMPOSE} down -v")

@task
def logs(c):
    """Стрим логов сервиса api."""
    c.run(f"{COMPOSE} logs -f {SERVICE}")

@task
def ps(c):
    """Статус контейнеров."""
    c.run(f"{COMPOSE} ps")


# ===== Alembic =====
@task(help={"m": "migration message, e.g. 'init schema'"})
def db_revision(c, m="new migration"):
    """Создать новую миграцию (autogenerate)."""
    c.run(
        f'{COMPOSE} exec {SERVICE} uv run alembic revision --autogenerate -m "{m}"'
    )

@task
def db_up(c):
    """Применить все миграции."""
    c.run(f"{COMPOSE} exec {SERVICE} uv run alembic upgrade head")

@task
def db_down(c):
    """Откатить одну миграцию назад."""
    c.run(f"{COMPOSE} exec {SERVICE} uv run alembic downgrade -1")

@task
def db_history(c):
    """Показать историю миграций."""
    c.run(f"{COMPOSE} exec {SERVICE} uv run alembic history --verbose")

@task
def db_current(c):
    """Показать текущую ревизию."""
    c.run(f"{COMPOSE} exec {SERVICE} uv run alembic current")


# ===== Tests =====
@task
def tests(c):
    """Запустить pytest внутри контейнера."""
    c.run(f"{COMPOSE} exec {SERVICE} uv run pytest")
