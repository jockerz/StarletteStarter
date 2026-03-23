import asyncio
from datetime import datetime
from typing import Any

from saq import CronJob, Queue
from saq.types import Context

from apps.core.configs import configs
from apps.extensions.db import create_db_engine, create_db_session
from apps.extensions.mail import send_message
from apps.extensions.saq import create_queue


async def cron(ctx: Context):
    print(f'{datetime.now().isoformat()}')


async def startup(ctx):
    # Configs
    ctx["config"] = configs

    # db
    db_engine = create_db_engine(configs.DATABASE_URL)
    ctx["db_engine"] = db_engine
    ctx["db_session"] = create_db_session(db_engine)


async def shutdown(ctx):
    await ctx["db_engine"].dispose()


async def before_process(ctx):
    ctx['db'] = ctx['db_session']()


async def after_process(ctx):
    await ctx['db'].close()


settings = {
    'queue': create_queue(configs),
    'functions': [
        send_message
    ],
    'concurrency': 2,
    'cron_jobs': [
        CronJob(cron, cron="* * * * * */5")
    ],
    'startup': startup,
    'shutdown': shutdown,
    'before_process': before_process,
    'after_process': after_process,
}
