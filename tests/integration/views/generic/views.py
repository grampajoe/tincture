"""
Views for tincture.views.generic tests.
"""
from tincture.views.generic.detail import DetailView

from tests.db import session

from .models import Person


class PersonView(DetailView):
    model = Person
    session = session
