from arq import ArqRedis, create_pool
from arq.connections import RedisSettings

from apps.core.configs import Base


async def create_connection(configs: Base) -> ArqRedis:
    return await create_pool(RedisSettings(
        host=configs.REDIS_HOST,
        port=configs.REDIS_PORT,
        username=configs.REDIS_USER,
        password=configs.REDIS_PASS,
        database=configs.REDIS_DB_ARQ
    ))
