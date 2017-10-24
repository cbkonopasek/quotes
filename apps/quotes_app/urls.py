from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^users/(?P<num>\d)$', views.user),

    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^add_quote$', views.add_quote),
    url(r'^logout$', views.logout),
    url(r'^like$', views.like),
    url(r'^unlike$', views.unlike),

]