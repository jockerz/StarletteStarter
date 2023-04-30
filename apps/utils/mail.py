from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Message:
    @staticmethod
    def create_plain(
        mail_to: str, subject: str, content: str,
        mail_from: str = 'noreply@mail'
    ) -> EmailMessage:
        """Build EmailMessage instance"""
        message = EmailMessage()
        message["From"] = mail_from
        message["To"] = mail_to
        message["Subject"] = subject
        message.set_content(content)
        return message

    @staticmethod
    def create_html(
        mail_to: str, subject: str, plain: str, html: str,
        mail_from: str = 'noreply@mail',
    ) -> MIMEMultipart:
        msg_text = MIMEText(plain, "plain", "utf-8")
        msg_html = MIMEText(html, "html", "utf-8")

        message = MIMEMultipart("alternative")
        message["From"] = mail_from
        message["To"] = mail_to
        message["Subject"] = subject
        message.attach(msg_text)
        message.attach(msg_html)
        return message
