from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart

from apps.utils.mail import Message


class TestMessage:
    def test_create_plain(self):
        mail = Message.create_plain(
            mail_to='to@mail.com', mail_from='from@mail.com',
            subject='Subject', content='content'
        )
        assert isinstance(mail, EmailMessage)
        assert 'To: to@mail.com' in str(mail)
        assert 'From: from@mail.com' in str(mail)
        assert 'Subject: Subject' in str(mail)
        assert '\ncontent\n' in str(mail)
        assert mail.get_content_type() == 'text/plain'

    def test_create_html(self):
        mail = Message.create_html(
            mail_to='to@mail.com', mail_from='from@mail.com',
            subject='Subject', plain='plain', html='<p>html</p>'
        )
        items = dict(mail.items())
        assert isinstance(mail, MIMEMultipart)
        assert items['To'] == 'to@mail.com'
        assert items['From'] == 'from@mail.com'
        assert items['Subject'] == 'Subject'
        assert mail.get_content_type() == 'multipart/alternative'
