from saq import Queue

from apps.core.configs import Base


def create_queue(config: Base) -> Queue:
    return Queue.from_url(
        f'redis://{config.REDIS_USER}'
        f':{config.REDIS_PASS}'
        f'@{config.REDIS_HOST}'
        f':{config.REDIS_PORT}'
        f'/{config.REDIS_DB_ARQ}'
    )
