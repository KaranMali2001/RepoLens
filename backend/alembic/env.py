from logging.config import fileConfig


from sqlalchemy import pool
from app.config.database import Base
from alembic import context
from app.config.config import settings
from app.models import *
from sqlalchemy.ext.asyncio import async_engine_from_config
import asyncio

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migration():
    print(config.get_section(config.config_ini_section))
    connectable = async_engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL.replace("%", "%%"),
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:

    asyncio.run(run_async_migration())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
