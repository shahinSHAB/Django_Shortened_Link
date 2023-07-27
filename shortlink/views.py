from django.http import Http404
from django.views.generic import CreateView, DetailView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect

from .models import Url, ShortUrl
from .forms import UrlForm
from .utils import create_short_link


class CreateShortUrl(LoginRequiredMixin, CreateView):
    model = Url
    form_class = UrlForm
    login_url = reverse_lazy('login')
    template_name = 'shortlink/index.html'

    def get_success_url(self):
        return reverse_lazy('shortlink:short_url', kwargs={'pk': self.url_id})

    def form_valid(self, form):
        form = form.save(commit=False)
        long_url_obj = Url.objects.filter(long_url=form.long_url)
        url_obj_exist = long_url_obj.exists()
        if url_obj_exist:
            self.url_id = long_url_obj.first().id
            return super().form_valid(form)
        short_link_obj = ShortUrl.objects.create(
            short_link=create_short_link(),
        )
        form.short_url = short_link_obj
        form.save()
        self.url_id = form.id
        return super().form_valid(form)


class ShortUrlView(LoginRequiredMixin, DetailView):
    template_name = 'shortlink/short_link.html'
    login_url = reverse_lazy('login')
    context_object_name = 'url'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Url.objects.all().select_related('short_url')


class ShortUrlRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = kwargs['short_url']
        short_url_obj = ShortUrl.objects.get(short_link=short_url)
        url_obj = Url.objects.get(short_url=short_url_obj)
        if not (short_url and short_url_obj):
            raise Http404('shortened link was broken, create another one')
        dif = timezone.now() - url_obj.created
        if dif.days > short_url_obj.exp_date:
            url_obj.delete()
            short_url_obj.delete()
            raise Http404('shortened link was expired, create another one')
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') or \
                    self.request.META['REMOTE_ADDR']
        short_url_obj.count += 1
        short_url_obj.event_time = timezone.now()
        short_url_obj.user_ip = ip
        short_url_obj.save()
        return url_obj.long_url
