=========================
Class-based generic views
=========================

.. note::
    This documentation only documents the *differences* between `Django`_ and
    Tincture. For all other functionality, see `Django's documentation`_.

Mixins
======

Single object mixins
--------------------

.. currentmodule:: tincture.views.generic.detail

SingleObjectMixin
~~~~~~~~~~~~~~~~~
.. class:: SingleObjectMixin()

    .. attribute:: model

        The SQLAlchemy model that this view will display data for. Specifying
        ``model = Foo`` is effectively the same as specifying
        ``query_object = session.query(Foo)``.

    .. attribute:: query_object

        A SQLAlchemy Query object.

        See `Django's SingleObjectMixin.queryset`_.

    .. attribute:: session

        A SQLAlchemy Session instance. This session will be used to generate
        a Query object for the view.

    .. attribute:: pk_url_kwargs

        A tuple of URLconf keword argument names that comprise the primary
        key. The default is ``('pk',)``. Note that this is named differently
        from `Django's SingleObjectMixin.pk_url_kwarg`_.

    .. method:: get_object(query_object=None)

        Returns the single object this view will display. If ``query_object``
        is provided, it will be used to obtain the object. Otherwise,
        :meth:`~SingleObjectMixin.get_query_object` will be used.

    .. method:: get_query_object()

        Returns the SQLAlchemy Query object that represents the data this view
        will display.

        See `Django's SingleObjectMixin.get_queryset`_.

SingleObjectTemplateResponseMixin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. class:: SingleObjectTemplateResponseMixin()

    .. method:: get_template_names()

        Returns a list of template names. In addition to the template names
        from Django that aren't based on the model, this returns:

        * ``<lowercase model class name><template_name_suffix>.html``

        .. note::
            With SQLAlchemy there's no built-in way to detect an app name,
            so you may want to provide your own implementation of this method
            to make template discovery more robust.

        See `Django's SingleObjectTemplateResponseMixin.get_template_names`_.

Multiple object mixins
----------------------

.. currentmodule:: tincture.views.generic.list

MultipleObjectMixin
~~~~~~~~~~~~~~~~~~~
.. class:: MultipleObjectMixin()

    .. attribute:: model

        The SQLAlchemy model that this view will display data for. Specifying
        ``model = Foo`` is effectively the same as specifying
        ``query_object = session.query(Foo)``.

    .. attribute:: query_object

        A SQLAlchemy Query object.

        See `Django's MultipleObjectMixin.queryset`_.

    .. attribute:: session

        A SQLAlchemy Session instance. This session will be used to generate
        a Query object for the view.

    .. method:: get_query_object()

        Returns the SQLAlchemy Query object that represents the data this view
        will display.

        See `Django's MultipleObjectMixin.get_queryset`_.

    .. method:: paginate_query_object(query_object, page_size)

        See `Django's MultipleObjectMixin.paginate_queryset`_.

    .. method:: get_paginate_by(query_object)

        See `Django's MultipleObjectMixin.get_paginate_by`_.

    .. method:: get_paginator(query_object, per_page, orphans=0, allow_empty_first_page=True)

        See `Django's MultipleObjectMixin.get_paginator`_.

    .. method:: get_context_object_name(object_list)

        Returns the context variable name that will be used to contain the
        list of data that this view is manipulating. If object_list is a
        SQLAlchemy Query object, it'll use the lowercased name of the first
        entity in the query. For example, a query for the Person and Dog
        models will return 'person_list'.

Generic views
=============

Detail views
------------

DetailView
~~~~~~~~~~
.. class:: BaseDetailView()
.. class:: DetailView()

    See `Django's DetailView`_.

    **Mixins**

    * :class:`tincture.views.generic.detail.SingleObjectMixin`
    * :class:`tincture.views.generic.detail.SingleObjectTemplateResponseMixin`


.. _Django: http://djangoproject.com
.. _Django's Documentation: http://docs.djangoproject.com/en/1.4/

.. _Django's SingleObjectMixin.queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.SingleObjectMixin.queryset
.. _Django's SingleObjectMixin.pk_url_kwarg: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg
.. _Django's SingleObjectMixin.get_queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.SingleObjectMixin.get_queryset

.. _Django's SingleObjectTemplateResponseMixin.get_template_names: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.SingleObjectTemplateResponseMixin.get_template_names

.. _Django's MultipleObjectMixin.queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.queryset
.. _Django's MultipleObjectMixin.get_queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.get_queryset
.. _Django's MultipleObjectMixin.paginate_queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.paginate_queryset
.. _Django's MultipleObjectMixin.get_paginate_by: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.get_paginate_by
.. _Django's MultipleObjectMixin.get_paginator: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.get_paginator

.. _Django's DetailView: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.DetailView
