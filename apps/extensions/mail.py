import aiosmtplib

from apps.core.configs import Base
from apps.utils.mail import Message


async def send_message(
    ctx: dict,
    recipient: str,
    subject: str,
    html: str,
    plain: str,
):
    """Send email via smtp"""
    config: Base = ctx['config']
    message = Message.create_html(
        mail_to=recipient, subject=subject, html=html, plain=plain,
    )

    await aiosmtplib.send(
        message,
        hostname=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        use_tls=config.SMTP_SSL,
        start_tls=False if config.SMTP_SSL else config.SMTP_START_SSL
    )
