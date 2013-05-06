"""
Integration tests for generic detail views.
"""
from django.test import TestCase
from django.conf import settings
from fixture import SQLAlchemyFixture, NamedDataStyle

from tests.db import session, setup_environment

from . import models
from . import fixtures


settings.INSTALLED_APPS = (
    settings.INSTALLED_APPS + ('tests.integration.views.generic',))


class TestListView(TestCase):
    """Tests for DetailView."""
    urls = 'tests.integration.views.generic.urls'

    def setUp(self):
        setup_environment()

        self.fixture = SQLAlchemyFixture(
            env=models,
            session=session,
            style=NamedDataStyle(),
        )

    def test_list_view(self):
        """Test the list view."""
        with self.fixture.data(fixtures.PersonData) as data:
            response = self.client.get('/people/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(data.PersonData.John.name, response.content)

    def test_list_view_allow_empty(self):
        """Test getting an empty list with allow_empty = True."""
        response = self.client.get('/people/')

        self.assertEqual(response.status_code, 200)

    def test_list_view_404(self):
        """Test getting an empty list with allow_empty = False."""
        response = self.client.get('/non_empty_people/')

        self.assertEqual(response.status_code, 404)
