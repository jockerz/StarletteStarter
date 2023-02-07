from apps.core.configs import configs
from apps.extensions.application import create_application


application = create_application(config=configs)
