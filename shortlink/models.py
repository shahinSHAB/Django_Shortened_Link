from django.db import models
from django.utils import timezone


class ShortUrl(models.Model):
    count = models.PositiveIntegerField(default=0)
    short_link = models.CharField(max_length=15, unique=True, blank=True)
    event_time = models.DateTimeField(default=timezone.now)
    exp_date = models.SmallIntegerField(default=90)
    user_ip = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f'short link is {self.short_link}'


class Url(models.Model):
    long_url = models.URLField(max_length=300)
    short_url = models.OneToOneField(ShortUrl, on_delete=models.SET_NULL,
                                     null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return f'URL is {self.long_url}'
