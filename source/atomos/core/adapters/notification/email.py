import ssl
import smtplib
import logging
from typing import List
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from atomos.core import config
from atomos.core.adapters.notification import template, notification

logger = logging.getLogger(__name__)

DEFAULT_HOST = config.SMTP_HOST
DEFAULT_PORT = config.SMTP_PORT
DEFAULT_USER = config.SMTP_USER
DEFAULT_PASSWORD = config.SMTP_PASSWORD
DEFAULT_TLS_MODE = config.ENVIRONMENT != 'development'


class MIMEMultipartBuilder:
    def __init__(self):
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Service Notification'
        message['From'] = DEFAULT_USER
        self._message = message

        self._html = template.template('')
        self._plain = ''

    def receiver(self, receiver: str):
        self._message['To'] = receiver
        return self

    def subject(self, subject: str):
        self._message['Subject'] = subject
        return self

    def html(self, content: str):
        self._html = template.template(content)
        return self

    def plain(self, content: str):
        self._plain = content
        return self

    def attachment(self, path: Path):
        with open(path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        # Encode file in ASCII characters
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header('content-disposition', 'attachment', filename=path.name)
        self._message.attach(part)
        return self

    def build(self) -> MIMEMultipart:
        self._message.attach(MIMEText(self._plain, 'plain'))
        self._message.attach(MIMEText(self._html, 'html'))
        return self._message


class EMailNotification(notification.Notification):
    def __init__(
        self,
        smtp_host=DEFAULT_HOST,
        smtp_port=DEFAULT_PORT,
        smtp_email=DEFAULT_USER,
        smtp_password=DEFAULT_PASSWORD,
        tls: bool = DEFAULT_TLS_MODE,
    ):
        self.host = smtp_host
        self.port = smtp_port
        self.email = smtp_email
        self.password = smtp_password
        self.tls = tls
        if tls:
            self.context = ssl.create_default_context()

    async def notify(self, destination: str, message: str):
        self.send([destination], message)

    async def broadcast(self, destinations: List[str], message: str):
        self.send(destinations, message)

    def send(self, destinations: List[str], message: str):
        mime = MIMEMultipartBuilder().plain(message).html(message).build()
        smtp: smtplib.SMTP = None
        try:
            smtp = smtplib.SMTP(self.host, self.port)
            if self.tls:
                smtp.ehlo()
                smtp.starttls(self.context)
                smtp.ehlo()
                smtp.login(self.email, self.password)

            smtp.sendmail(
                from_addr=self.email,
                to_addrs=destinations,
                msg=mime.as_string(),
            )
        except Exception as e:
            logger.error(e)
        finally:
            if smtp:
                smtp.quit()
