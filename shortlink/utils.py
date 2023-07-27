from collections.abc import Sequence
import random as rnd
from string import ascii_letters, digits
from django.conf import settings
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
CHARS = getattr(settings, 'CHARS', ascii_letters + digits)
SHORT_LINK_LENGTH = getattr(settings, 'LINK_LENGTH', 8)


def create_short_link(chars=CHARS, length=SHORT_LINK_LENGTH):
    short_link = ''.join(rnd.choice(chars) for _ in range(length))
    return short_link
