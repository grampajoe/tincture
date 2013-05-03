"""
Unit tests for tincture.views.generic.detail
"""
import unittest
import mock

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

from sqlalchemy.orm.exc import NoResultFound

from tincture.views.generic.detail import (
    SingleObjectMixin, SingleObjectTemplateResponseMixin)


class TestSingleObjectMixin(unittest.TestCase):
    """Tests for SingleObjectMixin."""
    def test_get_query_object(self):
        """Test getting a query object."""
        mixin = SingleObjectMixin()
        mixin.query_object = mock.sentinel.query_object

        query_object = mixin.get_query_object()

        self.assertIs(query_object, mixin.query_object)

    def test_get_query_object_model(self):
        """Test getting a query object from a model."""
        mixin = SingleObjectMixin()
        mixin.model = mock.Mock()
        mixin.session = mock.Mock()

        query_object = mixin.get_query_object()

        mixin.session.query.assert_called_with(mixin.model)
        self.assertIs(query_object, mixin.session.query.return_value)

    def test_get_query_object_none(self):
        """Test not providing query_object or model."""
        mixin = SingleObjectMixin()

        self.assertRaises(ImproperlyConfigured, mixin.get_query_object)

    def test_get_query_object_no_session(self):
        """Test not providing a session."""
        mixin = SingleObjectMixin()
        mixin.model = mock.Mock()

        self.assertRaises(ImproperlyConfigured, mixin.get_query_object)

    def test_get_object(self):
        """Test getting an object."""
        mixin = SingleObjectMixin()
        mixin.kwargs = {'pk': mock.sentinel.pk}
        query_object = mock.Mock()

        mixin.get_query_object = mock.Mock(return_value=query_object)

        obj = mixin.get_object()

        query_object.get.assert_called_with((mock.sentinel.pk,))
        self.assertIs(obj, query_object.get.return_value,
                      'Should return query_object.get().')

    def test_get_object_missing_kwargs(self):
        """Test getting an object with missing URLconf kwargs.

        It should fall back to using the slug.
        """
        mixin = SingleObjectMixin()
        mixin.kwargs = {'test': mock.sentinel.test,
                        'slug': mock.sentinel.slug}
        mixin.pk_url_kwargs = ('test', 'another')

        query_object = mock.Mock()
        query_object.filter.return_value = query_object

        mixin.get_query_object = mock.Mock(return_value=query_object)

        obj = mixin.get_object()

        query_object.filter.assert_called_with(
            **{mixin.slug_field: mixin.kwargs['slug']})
        self.assertIs(obj, query_object.one.return_value,
                      'Should call .one() to retrieve the object.')

    def test_get_object_missing_everything(self):
        """Test getting an object with no pk or slug."""
        mixin = SingleObjectMixin()
        mixin.kwargs = {}

        mixin.get_query_object = mock.Mock()

        self.assertRaises(AttributeError, mixin.get_object)

    def test_get_object_not_found(self):
        """Test getting a nonexistent object."""
        mixin = SingleObjectMixin()
        mixin.kwargs = {'pk': 'test'}

        query_object = mock.Mock()
        query_object.get.return_value = None

        mixin.get_query_object = mock.Mock(return_value=query_object)

        self.assertRaises(Http404, mixin.get_object)

    def test_get_object_pass_query(self):
        """Test passing a query object to get_object."""
        mixin = SingleObjectMixin()
        mixin.kwargs = {'pk': 'test'}

        query_object = mock.Mock()

        obj = mixin.get_object(query_object=query_object)

        self.assertIs(obj, query_object.get.return_value)

    def test_get_context_object_name(self):
        """Test the get_context_object_name method."""
        mixin = SingleObjectMixin()
        obj = mock.Mock()

        name = mixin.get_context_object_name(obj)

        self.assertEqual(name, obj.__class__.__name__.lower())

    def test_get_context_object_name_provided(self):
        """Test manually providing a context object name."""
        mixin = SingleObjectMixin()
        mixin.context_object_name = mock.sentinel.name

        name = mixin.get_context_object_name(None)

        self.assertEqual(name, mixin.context_object_name)


class TestSingleTemplateMixin(unittest.TestCase):
    """Tests for SingleObjectTemplateResponseMixin."""
    def setUp(self):
        self.mixin = SingleObjectTemplateResponseMixin()
        self.mixin.object = mock.Mock(spec=object)

    def test_get_template_names(self):
        """Test getting template names."""
        class Thingy:
            """A thingy."""
            pass
        self.mixin.object = Thingy()

        names = self.mixin.get_template_names()

        self.assertIn('thingy_detail.html', names)
