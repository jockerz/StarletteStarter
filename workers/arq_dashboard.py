from arq_dashboard.core import settings
from arq_dashboard.main import create_app
from arq.constants import default_queue_name

from apps.core.configs import configs
from apps.extensions.arq import create_setting


settings.ARQ_QUEUES[default_queue_name] = create_setting(configs)

app = create_app()
