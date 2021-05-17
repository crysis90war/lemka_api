import random
import string
import threading

from django.core.mail import EmailMessage

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Utils:
    @staticmethod
    def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def generate_random_numbers():
        randomnumber = random.randint(0, 999999)
        return "".join(str(randomnumber))

    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.content_subtype = "html"
        EmailThread(email).start()
