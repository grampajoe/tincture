from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage
from django.http import Http404

from django.views.generic.list import MultipleObjectMixin


class MultipleObjectMixin(MultipleObjectMixin):
    """A mixin for multiple objects."""
    query_object = None
    session = None

    def get_query_object(self):
        """Get the list of items for this view."""
        if self.query_object is not None:
            return self.query_object
        elif self.model is not None:
            if self.session is None:
                raise ImproperlyConfigured(
                    '%(cls)s is missing a session. Define %(cls)s.session '
                    'or %(cls)s.query_object.'
                    % {'cls': self.__class__.__name__})
            return self.session.query(self.model)
        else:
            raise ImproperlyConfigured(
                '%(cls)s is missing a query object. Define %(cls)s.model or '
                '%(cls)s.query_object, or override %(cls)s.get_object.'
                % {'cls': self.__class__.__name__})

    def paginate_query_object(self, query_object, page_size):
        """A wrapper around paginate_queryset with different names.

        This is a dirty trick that may not always work. If paginate_queryset
        turns out not to be optimal for SQLAlchemy query objects, the fix
        may be as simple as replacing Paginator as the default paginator
        class.
        """
        return self.paginate_queryset(query_object, page_size)

    def get_context_object_name(self, object_list):
        """Get the name of the context object for this view.

        If a query object is provided, its first entity's class name
        will be used. This could be weird, so you might want to provide
        your own name.
        """
        if self.context_object_name is not None:
            return self.context_object_name
        elif hasattr(object_list, '_entity_zero'):
            # Use the first entity's class name
            entity = object_list._entity_zero()
            name = '%s_list' % entity.type.__name__.lower()
            return name
        else:
            return None

    def get_context_data(self, **kwargs):
        """Get context data for the view."""
        query_object = kwargs.pop('object_list')
        page_size = self.get_paginate_by(query_object)
        context_object_name = self.get_context_object_name(query_object)

        if page_size:
            paginator, page, query_object, is_paginated = \
                self.paginate_query_object(query_object, page_size)

            context = {
                'paginator': paginator,
                'page': page,
                'object_list': query_object,
                'is_paginated': is_paginated,
            }
        else:
            context = {
                'paginator': None,
                'page': None,
                'object_list': query_object,
                'is_paginated': None,
            }

        context.update(kwargs)

        if context_object_name is not None:
            context[context_object_name] = query_object

        return context
