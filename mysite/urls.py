from django.conf.urls import url, include
from . import views
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', views.criteria, name='criteria'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^(\D+)$', views.match_details, name='match_details'),

]
