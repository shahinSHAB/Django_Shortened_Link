from django.contrib import admin
from . models import Url, ShortUrl


admin.site.register(Url)
admin.site.register(ShortUrl)
