from django.core.exceptions import ImproperlyConfigured
from django.http import Http404

from django.views.generic.detail import (
    SingleObjectMixin, BaseDetailView, SingleObjectTemplateResponseMixin)

from sqlalchemy.orm.exc import NoResultFound


class SingleObjectMixin(SingleObjectMixin):
    """An analog to Django's SingleObjectMixin."""
    query_object = None
    session = None
    pk_url_kwargs = ('pk',)

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

    def get_context_object_name(self, obj):
        """Get the object's context name."""
        if self.context_object_name:
            return self.context_object_name
        else:
            return obj.__class__.__name__.lower()


class BaseDetailView(SingleObjectMixin, BaseDetailView):
    pass


class SingleObjectTemplateResponseMixin(SingleObjectTemplateResponseMixin):
    def get_template_names(self):
        """Return a list of template names."""
        names = super(SingleObjectTemplateResponseMixin,
                     self).get_template_names()

        names.append('%(name)s%(suffix)s.html' % {
            'name': self.object.__class__.__name__.lower(),
            'suffix': self.template_name_suffix,
        })

        return names
