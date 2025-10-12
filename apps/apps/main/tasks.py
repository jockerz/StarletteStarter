import typing as t

from saq import Queue
from starlette.datastructures import URL

from apps.core.logger import get_logger
from apps.utils.mail import Message

logger = get_logger()


TPL_ACTIVATION_EMAIL_HTML = """\
<p>Go to <a href="{activation_url}">Activation Page</a></p>
<p>Or you can to to this URL <strong>{activation_url}</strong></p> 
"""
TPL_ACTIVATION_EMAIL_TEXT = """\
Your activation URL is {activation_url}
"""
TPL_RESET_EMAIL_HTML = """\
<p>Go to <a href="{reset_url}">Password Reset Page</a></p>
<p>Or you can to to this URL <strong>{reset_url}</strong></p> 
"""
TPL_RESET_EMAIL_TEXT = """\
Your password reset URL is {reset_url}
"""


async def send_activation_message(
    saq: Queue, recipient: str, activation_url: t.Union[str, URL]
):
    message = Message.create_html(
        mail_to=recipient,
        subject="Activation URL",
        html=TPL_ACTIVATION_EMAIL_HTML.format(activation_url=activation_url),
        plain=TPL_ACTIVATION_EMAIL_TEXT.format(activation_url=activation_url),
    )
    logger.debug(f'sending activation email to={recipient}')
    await saq.enqueue("send_message", message=message)


async def send_reset_password(
    saq: Queue, recipient: str, reset_url: URL
):
    message = Message.create_html(
        mail_to=recipient,
        subject="Password Reset URL",
        html=TPL_RESET_EMAIL_HTML.format(reset_url=reset_url),
        plain=TPL_RESET_EMAIL_TEXT.format(reset_url=reset_url),
    )
    logger.debug(f'sending reset email to={recipient}')
    await saq.enqueue("send_message", message=message)
