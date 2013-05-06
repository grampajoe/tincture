from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^people/$', views.PeopleView.as_view(), name='people'),
    url(r'^non_empty_people/$', views.NonEmptyPeopleView.as_view(),
        name='non_empty_people'),
    url(r'^people/(?P<pk>\d+)/$', views.PersonView.as_view(), name='person'),
)
