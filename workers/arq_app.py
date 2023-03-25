from apps.core.configs import configs
from apps.extensions.arq import create_setting
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

    redis_settings = create_setting(configs)
