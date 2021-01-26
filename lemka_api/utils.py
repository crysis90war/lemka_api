import random
import string

from PIL import Image
from django.core.mail import EmailMessage

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6


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
        email.send()

    @staticmethod
    def resize_image(img_path, img_size):
        img = Image.open(img_path)
        if img.width > img_size[0] or img.height > img_size[1]:
            img.thumbnail(img_size)
            img.save(img_path)
