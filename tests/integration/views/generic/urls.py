from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^people/(?P<pk>\d+)/$', views.PersonView.as_view(), name='person'),
)
