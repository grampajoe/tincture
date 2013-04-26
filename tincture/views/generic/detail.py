from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

from sqlalchemy.orm.exc import NoResultFound


class SingleObjectMixin(object):
    """An analog to Django's SingleObjectMixin."""
    model = None
    query_object = None
    session = None
    pk_url_kwargs = ('pk',)
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, query_object=None):
        """Returns the object the view is displaying."""
        if query_object is None:
            query_object = self.get_query_object()

        pk = tuple(self.kwargs.get(name, None)
                   for name in self.pk_url_kwargs)
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        try:
            if None not in pk:
                obj = query_object.get(pk)
            elif slug is not None:
                # Use one() since the slug is assumed to be unique
                obj = query_object.filter(**{self.slug_field: slug}).one()
            else:
                raise AttributeError(
                    'Generic detail view %s must be called with either an '
                    'object pk or slug.' % self.__class__.__name__)
        except NoResultFound as e:
            raise Http404(e)

        return obj

    def get_query_object(self):
        """Get the query object to use for object lookup."""
        if self.query_object is None:
            if self.session is None:
                raise ImproperlyConfigured(
                    '%(cls)s is missing a session. Define %(cls)s.session '
                    'or %(cls)s.query_object.'
                    % {'cls': self.__class__.__name__})

            if self.model:
                return self.session.query(self.model)
            else:
                raise ImproperlyConfigured(
                    '%(cls)s is missing a query object. Define %(cls)s.model or '
                    '%(cls)s.query_object, or override %(cls)s.get_object.'
                    % {'cls': self.__class__.__name__})
        return self.query_object
