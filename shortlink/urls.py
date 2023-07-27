from django.urls import path

from . import views


app_name = 'shortlink'

urlpatterns = [
    path('', views.CreateShortUrl.as_view(), name='create_url'),
    path('short-link/<int:pk>/', views.ShortUrlView.as_view(),
         name='short_url'),
    path('short-link/<str:short_url>/', views.ShortUrlRedirect.as_view(),
         name='url_redirect'),
]
