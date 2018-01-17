from django.conf.urls import url, include
from . import views
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', views.criteria, name='home'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^GetData/', views.GetData, name='GetData'),
    url(r'^matches_list\.html$', views.matches_list, name='matches_list'),
    url(r'^(\D+)$', views.match_details, name='match_details'),

]
