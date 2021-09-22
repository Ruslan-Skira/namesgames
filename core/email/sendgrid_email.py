"""
Send emails using SendGrid API.
"""
import logging
import threading
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.base import BaseEmailBackend
from python_http_client import exceptions
from python_http_client.client import Response
from sendgrid import Mail, SendGridAPIClient

log = logging.getLogger(__name__)


class EmailSendgridBackend(BaseEmailBackend):
    """
    Send emails via SendGrid API using a helper class, 'SendGidAPIClient'.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, fail_silently=False, **kwargs):
        """
        Instance should contain all the attributes necessary to send an email.

        Reference:
            SendGrid API POST method (v.3):
            https://docs.sendgrid.com/api-reference/how-to-use-the-sendgrid-v3-api/requests

        Arguments:
            to_email (str): user's email a message will be sent to.
            to_name (str): username.
            from_email (str): Sender's email, e.g.
            from_name (str): Sender's name, e.g.
            reply_to (str): An email a user can reply to, e.g. "need_to_create_support@email.com"
            subject (str): Global subject of an email. Being a required POST parameter,
                will not override the one defined in a template.
            api_key (str): General SendGrid API key, necessary to perform authorized  requests.
            templates_resolver (SendGridTemplateResolver): an object of SendGridTemplateResolver class,
                which will be used to define the SendGrid template id to use.
            content (str): body of the message.
        """
        super().__init__(fail_silently=fail_silently)
        self.api_key = settings.SENDGRID_API_KEY
        self._lock = threading.RLock()

    @staticmethod
    def personalize_email(e_message: EmailMessage) -> Mail:
        """
        User set custom parameters to send email with using SendGrid API.
        Returns:
            mail(sendgrid.helpers.mail.Mail): Mail object containing
                all the necessary email parameters, i.e. message per se.

        """
        if e_message:
            mail = Mail(
                from_email=settings.EMAIL_ADMIN,
                to_emails=e_message.to[0],
                subject=e_message.subject,
                html_content=e_message.body,
            )

            log.info(f"A python-sendgrid Mail object has been created: {mail}")

            return mail
        log.info("The django EmailMessage object are not created")

    def send_sendgrid_email(self, mail: Mail) -> Response:

        """
        Send an email using a 'sendgrid' helper class,  'SendGidAPIClient'.

        Reference:
            'sendgrid' library: https://github.com/sendgrid/sendgrid-python

        Arguments:

            self (): SendGridEmailProvider object.
            mail (sendgrid.helpers.mail.Mail): Mail object containing
            all the necessary email parameters, i.e. message per se.

        Returns:
            response (python_http_client.client.Response): Response object.
        """

        try:
            sg_client = SendGridAPIClient(api_key=self.api_key)
            response = sg_client.send(mail)

            if response.status_code == 202:
                log.debug("Successfully sent an email using SendGrid API.")
            else:
                log.error(
                    f"Failed to send and email using SendGrid API. "
                    f"Status code: {response.status_code}. "
                    f"Response body: {response.body}. "
                    f"Headers: {response.headers}"
                )
            return response
        except exceptions.HTTPError as e:
            if not self.fail_silently:
                log.error(
                    " An error occurred while sending an email using SendGrid API. "
                    f"Error message: SMTPException {e} "
                )
                raise SMTPException
            else:
                log.error(
                    " An error occurred while sending an email using SendGrid API. "
                    f"Error message: {e}"
                )

    def send_messages(self, email_messages):
        """
        Send one or more Mail object and return the number of email messages sent.
        Args:
            email_messages (list): list of EmailMessage objects

        Returns(int): amount of sent emails.

        """

        num_sent = 0
        if not email_messages:
            return 0
        elif email_messages:
            for e_message in email_messages:
                mail = self.personalize_email(e_message)
                sent = self.send_sendgrid_email(mail)
                if sent:
                    num_sent += 1
        return num_sent
