import typing as t
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from apps.core.configs import Base


async def send_message(
    ctx: dict, message: t.Union[EmailMessage, MIMEMultipart]
):
    """Send email via smtp"""
    config: Base = ctx['config']

    await aiosmtplib.send(
        message,
        hostname=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        use_tls=config.SMTP_SSL,
        start_tls=False if config.SMTP_SSL else config.SMTP_START_SSL
    )
