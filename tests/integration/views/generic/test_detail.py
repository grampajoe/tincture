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


class TestDetailView(TestCase):
    """Tests for DetailView."""
    urls = 'tests.integration.views.generic.urls'

    def setUp(self):
        setup_environment()

        self.fixture = SQLAlchemyFixture(
            env=models,
            session=session,
            style=NamedDataStyle(),
        )

    def test_detail_view(self):
        with self.fixture.data(fixtures.PersonData) as data:
            response = self.client.get('/people/%s/' % data.PersonData.John.id)

        self.assertEqual(response.status_code, 200)
        self.assertIn(data.PersonData.John.name, response.content)

    def test_detail_view_not_found(self):
        response = self.client.get('/people/100000000001/')

        self.assertEqual(response.status_code, 404)
