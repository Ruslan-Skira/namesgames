"""
Send emails using SendGrid API.
"""
import logging
from sendgrid.helpers.mail import Mail

log = logging.getLogger(__name__)


class SendGridEmailProvider:
    """
    Send emails via SendGrid API using a helper class, 'SendGidAPIClient'.
    """
    def send_sendgrid_email(self, mail):
        """
        Send an email using a 'sendgrid' helper class,  'SendGidAPIClient'.

        Reference:
            'sendgrid' library: https://github.com/sendgrid/sendgrid-python

        Arguments:
            mail (sendgrid.helpers.mail.Mail)

        """