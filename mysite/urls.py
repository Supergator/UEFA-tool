from django.conf.urls import url, include
from . import views
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^SetCriteria/', views.SetCriteria, name='SetCriteria'),
    url(r'^prepareDataForCountries/', views.prepareDataForCountries, name='prepareDataForCountries'),
    url(r'^GetClubs/', views.GetClubs, name='GetClubs'),
    #url(r'^matches_list\.html$', views.matches_list, name='matches_list'),
    url(r'^(\D+)$', views.load_page, name='load_page'),

]
