from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.criteria, name='criteria'),
    url(r'^(\D+)$', views.match_details, name='match_details'),
]
