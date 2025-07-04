import json
import typing as t
from dataclasses import dataclass, field

from jinja2.utils import pass_context
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from apps.utils.i18n import convert_lazy_string


FLASH_SESSION_NAME = '_flash'


@dataclass
class Notification:
    title: str
    icon: t.Literal[
        'info', 'success', 'error', 'warning', 'question'
    ] = field(default='info')
    text: str = field(default=None)
    footer: str = field(default=None)
    category: t.Literal['notification', 'alert'] = field(default='notification')

    def as_flash_data(self):
        json_data = convert_lazy_string(self.__dict__)
        return self.icon, json.dumps(json_data)

    @classmethod
    def pop(cls, request: Request, icon: str = None):
        """Pop notification from current session"""
        data = request.session.pop(FLASH_SESSION_NAME, []) or []
        if icon is None:
            return data
        else:
            return [(i, d) for (i, d) in data if i == icon]

    def push(self, request: Request):
        """Push a notification into current session"""
        data = self.pop(request)
        data.append(self.as_flash_data())
        request.session[FLASH_SESSION_NAME] = data

    @classmethod
    def push_multi(cls, request: Request, *notification):
        """Push one or more notifications"""
        data = cls.pop(request)
        for item in notification:
            data.append(item.as_flash_data())
        request.session[FLASH_SESSION_NAME] = data


def add_notification_filter(templates: Jinja2Templates):
    """Add notification as template function"""
    @pass_context
    def get_notification(context: dict, icon: str = None):
        request = context["request"]
        data = Notification.pop(request, icon)
        # only list notification data
        return json.dumps([d for (_, d) in data])

    templates.env.globals['get_notification'] = get_notification
