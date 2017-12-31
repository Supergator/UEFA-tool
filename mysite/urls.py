from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.match_details, name='match_details'),
]
