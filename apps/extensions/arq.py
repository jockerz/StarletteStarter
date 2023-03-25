from arq import ArqRedis, create_pool
from arq.connections import RedisSettings

from apps.core.configs import Base


def create_setting(config: Base) -> RedisSettings:
    return RedisSettings(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        username=config.REDIS_USER,
        password=config.REDIS_PASS,
        database=config.REDIS_DB_ARQ
    )


async def create_connection(config: Base) -> ArqRedis:
    return await create_pool(
        create_setting(config),
        # job_serializer=msgpack.packb,
        # job_deserializer=lambda b: msgpack.unpackb(b, raw=False),
    )
