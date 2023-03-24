import msgpack
from arq.connections import RedisSettings

from apps.core.configs import configs
from apps.extensions.db import create_db_engine, create_db_session
from apps.extensions.mail import send_message


async def startup(ctx):
    # Configs
    ctx["config"] = configs

    # db
    db_engine = create_db_engine(configs.DATABASE_URL)
    ctx["db_engine"] = db_engine
    ctx["db_session"] = create_db_session(db_engine)


async def shutdown(ctx):
    await ctx["db_engine"].dispose()


class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    cron_jobs = []
    functions = [
        send_message
    ]

    # job_serializer = msgpack.packb
    # job_deserializer = lambda b: msgpack.unpackb(b, raw=False)

    redis_settings = RedisSettings(
        host=configs.REDIS_HOST,
        port=configs.REDIS_PORT,
        username=configs.REDIS_USER,
        password=configs.REDIS_PASS,
        database=configs.REDIS_DB_ARQ
    )
