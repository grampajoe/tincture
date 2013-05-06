"""
Views for tincture.views.generic tests.
"""
from tincture.views.generic.detail import DetailView
from tincture.views.generic.list import ListView

from tests.db import session

from .models import Person


class PersonView(DetailView):
    """A detail view for a single person."""
    model = Person
    session = session


class PeopleView(ListView):
    """A list view for people."""
    model = Person
    session = session


class NonEmptyPeopleView(ListView):
    """A list view for people that's not allowed to be empty."""
    model = Person
    session = session
    allow_empty = False
