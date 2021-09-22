"""
Test SengGrid API.
"""

from django.core.mail import EmailMessage
from django.test import TestCase
from django.test.utils import override_settings
from unittest.mock import patch
from python_http_client import exceptions

from core.email.sendgrid_email import EmailSendgridBackend


class SendgridEmailProviderTest(TestCase):
    exception_http = exceptions.HTTPError("404", "potomychto", "body", "headers")

    def setUp(self) -> None:
        """
        Hook method for setting up the SendGridEmailProvider before exercising it.
        """
        self.sg_email_provider = EmailSendgridBackend(
            to_email="to_email",
            to_name="to_name",
            from_email="from_email",
            from_name="from_name",
            reply_ty="reply_to",
            subject="subject",
            api_key="api_key",
            context=None,
        )

        self.sg_email_provider_1 = EmailSendgridBackend(
            to_email="to_email",
            to_name="to_name",
            from_email="from_email",
            from_name="from_name",
            reply_ty="reply_to",
            subject="subject",
            api_key="api_key",
            context=None,
            fail_silently=True,
        )
        self.email_message = EmailMessage(to=["to_email@blabla.com"])
        self.email_message_1 = EmailMessage()

    def test_personalize_email(self) -> None:
        self.sg_email_provider.context = "text context"
        sg_email = self.sg_email_provider.personalize_email(self.email_message)
        sg_email_dict = sg_email.get()

        self.assertEqual(
            sg_email_dict["personalizations"][0]["to"][0]["email"],
            "to_email@blabla.com",
        )

    @patch("core.email.sendgrid_email.SendGridAPIClient.send")
    def test_send_email(self, send_email) -> None:
        """
        Test will mock the send() function and check does it called or not.
        Returns:

        """
        self.sg_email_provider.context = "text context"
        sg_email = self.sg_email_provider.personalize_email(self.email_message)
        self.sg_email_provider.send_sendgrid_email(sg_email)
        # Check send_email function was called
        send_email.assert_called()

    @override_settings(EMAIL_BACKEND="core.email.sendgrid_email.EmailSendgridBackend")
    @patch(
        "core.email.sendgrid_email.SendGridAPIClient.send", side_effect=exception_http
    )
    def test_send_email_fail_silent(self) -> None:
        self.sg_email_provider_1.context = "text context"
        from smtplib import SMTPException

        # The exception should rise
        with self.assertRaises(SMTPException):
            self.email_message.send(fail_silently=False)

    @override_settings(EMAIL_BACKEND="core.email.sendgrid_email.EmailSendgridBackend")
    @patch(
        "core.email.sendgrid_email.SendGridAPIClient.send", side_effect=exception_http
    )
    def test_send_email_fail_silent_true(self, send_email) -> None:
        # The exception should rise
        send_email.status_code.return_value = 202
        with self.assertLogs("core.email.sendgrid_email", level="ERROR") as cm:
            self.email_message.send(fail_silently=True)
        self.assertEqual(
            [
                "ERROR:core.email.sendgrid_email: An error occurred while sending an email using SendGrid API. Error message: ('404', 'potomychto', 'body', 'headers')"
            ],
            cm.output,
        )
