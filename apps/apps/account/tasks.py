from arq import ArqRedis

from apps.core.logger import get_logger
from apps.utils.mail import Message

logger = get_logger()


TPL_UPDATE_EMAIL_HTML = """\
<p>Go to <a href="{validation_url}">Email Update Page</a> save your email update.</p>
<p>Or you can go to this URL <strong>{validation_url}</strong></p> 
"""
TPL_UPDATE_EMAIL_TEXT = """\
Password update URL is {validation_url}
"""


async def send_validate_email(
    arq: ArqRedis, recipient: str, validation_url: str
):
    message = Message.create_html(
        mail_to=recipient,
        subject="Email update validation URL",
        html=TPL_UPDATE_EMAIL_HTML.format(validation_url=validation_url),
        plain=TPL_UPDATE_EMAIL_TEXT.format(validation_url=validation_url),
    )
    logger.debug(f'sending email update email to={recipient}')
    await arq.enqueue_job("send_message", message=message)
