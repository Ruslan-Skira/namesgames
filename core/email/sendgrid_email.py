"""
Send emails using SendGrid API.
"""
import logging

from python_http_client import exceptions
from python_http_client.client import Response
from sendgrid import SendGridAPIClient

log = logging.getLogger(__name__)


class SendGridEmailProvider:
    """
    Send emails via SendGrid API using a helper class, 'SendGidAPIClient'.
    """

    def __init__(
            self,
            to_email,
            to_name,
            from_email,
            from_name,
            reply_to,
            subject,
            api_key,
            templates_resolver,
            context=None):
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
        """
        self.to_email = to_email
        self.to_name = to_name
        self.from_email = from_email
        self.from_name = from_name
        self.reply_to = reply_to
        self.subject = subject
        self.api_key = api_key
        self.templates_resolver = templates_resolver
        self.context = context

    def send_sendgrid_email(self, mail: str) -> Response:

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
            client = SendGridAPIClient(api_key=self.api_key)
            response = client.send(mail)
            if response.status_code == 202:
                log.debug("Successfully sent an email using SendGrid API.")
            else:
                log.error(f"Failed to send and email using SendGrid API. "
                          f"Status code: {response.status_code}. "
                          f"Response body: {response.body}. "
                          f"Headers: {response.headers}"
                          )
            return response
        except exceptions.HTTPError as e:
            log.error(" An error occurred while sending an email using SendGrid API. "
                      f"Error message: {e}")
