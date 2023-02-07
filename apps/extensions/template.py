from datetime import datetime

from jinja2.utils import pass_context
from starlette.templating import Jinja2Templates

from apps.utils.notification import add_notification_filter


@pass_context
def path(context: dict):
    return context["request"]['raw_path'].decode('utf8')


@pass_context
def root_path(context: dict):
    return context["request"]['root_path']


@pass_context
def child_path(context: dict):
    return context["request"]['path']


templates = Jinja2Templates(directory='templates')
templates.env.globals['path'] = path
templates.env.globals['root_path'] = root_path
templates.env.globals['child_path'] = child_path

add_notification_filter(templates)


def datetime_format(value: datetime = None, fmt: str = "%d-%m-%Y %H:%M:%S"):
    if value is None:
        return ''
    return value.strftime(fmt)


templates.env.filters["datetime_format"] = datetime_format
