Class-based generic views
=========================

Many of `Django`_'s class-based generic views can be used with `SQLAlchemy`_
without modification. For those that don't, Tincture attempts to provide
substitutions.

The APIs of Tincture's generic views differ slightly from `Django`_'s, where
appropriate. For example, many of the views have a ``session`` attribute
that holds a `SQLAlchemy`_ ``Session`` object.


Simple Usage
------------

Say you have the following SQLAlchemy model::

    # some_app/models.py
    from sqlalchemy.orm import Column, Integer, String

    class Person(Base):
        __tablename__ = 'people'

        id = Column(Integer, primary_key=True)
        name = Column(String)

You could create a list view for ``Person`` objects much the same way as
with `Django's ListView`_, with the addition of the ``session`` attribute::

    # some_app/views.py
    from tincture.views.generic import ListView
    from some_app.models import Person

    # Assuming you have a db module with a session atrribute:
    import db

    class PersonListView(ListView):
        session = db.session
        model = Person

.. note::
    The session object can't be obtained automatically, so it must be provided or
    ``ImproperlyConfigured`` will be raised when the view tries to retrieve any
    model objects.

``PersonListView`` could then be added to your urlconf like any other
class-based view::

    # some_project/urls.py
    from django.conf.urls import patterns, url, include
    from some_app.views import PersonListView

    urlpatterns = patterns('',
        (r'^people/$', PersonListView.as_view()),
    )

.. _Django: http://djangoproject.com
.. _SQLAlchemy: http://sqlalchemy.org
.. _Django's ListView: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#listview
