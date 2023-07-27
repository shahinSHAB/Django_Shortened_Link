from django.forms.models import ModelForm
from .models import Url


class UrlForm(ModelForm):

    class Meta:
        model = Url
        fields = ('long_url', )
