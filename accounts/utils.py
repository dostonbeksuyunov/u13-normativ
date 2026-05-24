from threading import Thread

from django.core.mail import send_mail
from django.conf import settings


class EmailThread(Thread):

    def __init__(
        self,
        subject,
        message,
        recipient_list
    ):

        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list

        Thread.__init__(self)

    def run(self):

        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
        )


def send_email_thread(
    subject,
    message,
    recipient_list
):

    EmailThread(
        subject,
        message,
        recipient_list
    ).start()