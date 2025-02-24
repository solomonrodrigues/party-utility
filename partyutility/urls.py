# partyutility/urls.py
from django.urls import path

from partyutility.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]