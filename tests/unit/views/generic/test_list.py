"""
Unit tests for views.generic.list
"""
import unittest
import mock

from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage
from django.http import HttpResponse, Http404

from tincture.views.generic.list import (
    MultipleObjectMixin, BaseListView, MultipleObjectTemplateResponseMixin)


class TestMultipleObjectMixin(unittest.TestCase):
    def setUp(self):
        self.mixin = MultipleObjectMixin()
        self.mixin.request = mock.Mock(GET={}, POST={})
        self.mixin.kwargs = {}

    """Tests for MultipleObjectMixin."""
    def test_get_query_object(self):
        """Test getting a query object."""
        self.mixin.query_object = mock.Mock()

        query_object = self.mixin.get_query_object()

        self.assertIs(query_object, self.mixin.query_object)

    def test_get_query_object_model(self):
        """Test getting a query object from a model."""
        self.mixin.session = mock.Mock()
        self.mixin.model = mock.Mock()

        query_object = self.mixin.get_query_object()

        self.mixin.session.query.assert_called_with(self.mixin.model)
        self.assertIs(query_object, self.mixin.session.query.return_value)

    def test_get_query_object_model_no_session(self):
        """Test getting a query object from a model with no session."""
        self.mixin.model = mock.Mock()

        self.assertRaises(ImproperlyConfigured, self.mixin.get_query_object)

    def test_get_query_object_nothing(self):
        """Test getting a query object with nothing defined."""
        self.mixin.session = mock.Mock()

        self.assertRaises(ImproperlyConfigured, self.mixin.get_query_object)

    def test_get_context_object_name(self):
        """Test getting the context object name."""
        self.mixin.context_object_name = mock.sentinel.name

        object_list = mock.Mock()

        name = self.mixin.get_context_object_name(object_list)

        self.assertEqual(name, self.mixin.context_object_name)

    def test_get_context_object_name_query(self):
        """Test getting the context object name from a query object."""
        entity = mock.Mock()
        entity.type.__name__ = mock.Mock()
        query_object = mock.Mock()
        query_object._entity_zero.return_value = entity

        name = self.mixin.get_context_object_name(query_object)

        self.assertEqual(name, '%s_list' % entity.type.__name__.lower())

    def test_get_context_object_name_list(self):
        """Test getting a context object name from a list."""
        object_list = [1, 2, 3]

        name = self.mixin.get_context_object_name(object_list)

        self.assertIsNone(name)

    def test_paginate_query_object(self):
        """Test paginating a query object."""
        self.mixin.paginate_queryset = mock.Mock()

        query_object = mock.sentinel.query_object
        page_size = mock.sentinel.page_size

        result = self.mixin.paginate_query_object(query_object, page_size)

        self.mixin.paginate_queryset.assert_called_with(
            query_object, page_size)
        self.assertIs(result, self.mixin.paginate_queryset.return_value)

    def test_get_context_data(self):
        """Test getting context data."""
        self.mixin.get_paginate_by = mock.Mock(return_value=None)
        self.mixin.get_context_object_name = mock.Mock(return_value=None)
        self.mixin.paginate_query_object = mock.Mock()

        query_object = mock.sentinel.query_object

        context = self.mixin.get_context_data(
            object_list=query_object, fart=mock.sentinel.fart)

        self.assertIsInstance(context, dict)
        self.assertEqual({
            'paginator': None,
            'page': None,
            'object_list': query_object,
            'is_paginated': None,
            'fart': mock.sentinel.fart,
        }, context)

        # With pagination
        paginator = mock.sentinel.paginator
        page = mock.sentinel.page
        is_paginated = mock.sentinel.is_paginated

        self.mixin.get_paginate_by.return_value = 10
        self.mixin.paginate_query_object.return_value = (
            paginator, page, query_object, is_paginated
        )

        context = self.mixin.get_context_data(object_list=query_object)

        self.assertEqual({
            'paginator': paginator,
            'page': page,
            'object_list': query_object,
            'is_paginated': is_paginated,
        }, context)

        # With a context object name
        self.mixin.get_context_object_name.return_value = 'test'

        context = self.mixin.get_context_data(object_list=query_object)

        self.assertIs(context['test'], query_object)


class TestBaseListView(unittest.TestCase):
    """Tests for BaseListView."""
    def test_get(self):
        """Test the BaseListView.get."""
        view = BaseListView()
        view.render_to_response = mock.Mock()
        view.get_context_data = mock.Mock()
        view.get_query_object = mock.Mock()

        response = view.get(mock.sentinel.request)

        view.get_context_data.assert_called_with(
            object_list=view.get_query_object.return_value)

        view.render_to_response.assert_called_with(
            view.get_context_data.return_value)
        self.assertIs(response, view.render_to_response.return_value)

        self.assertIs(view.object_list, view.get_query_object.return_value)

    def test_get_no_allow_empty(self):
        """Test BaseListView.get with allow_empty = False."""
        view = BaseListView()
        view.allow_empty = False
        view.get_query_object = mock.Mock(return_value=[])

        self.assertRaises(Http404, view.get, mock.sentinel.request)


class TestMultipleObjectTemplateResponseMixin(unittest.TestCase):
    """Tests for MultipleObjectTemplateResponseMixin."""
    def test_get_template_names(self):
        """Test getting template names for multiple objects."""
        class Thingy(object):
            pass
        entity = mock.Mock()
        entity.type = Thingy

        class Query(object):
            _entity_zero = mock.Mock(return_value=entity)

        query_object = Query()

        mixin = MultipleObjectTemplateResponseMixin()
        mixin.object_list = query_object

        names = mixin.get_template_names()

        self.assertIn('thingy_list.html', names)

    def test_get_template_names_list(self):
        """Test getting template names with a list."""
        mixin = MultipleObjectTemplateResponseMixin()
        mixin.object_list = ['thing']

        names = mixin.get_template_names()

        self.assertEqual(names, [])
