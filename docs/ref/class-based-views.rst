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

    .. method:: get_object(query_object=None)

        Returns the single object this view will display. If ``query_object``
        is provided, it will be used to obtain the object. Otherwise,
        :meth:`~SingleObjectMixin.get_query_object` will be used.

    .. method:: get_query_object()

        Returns the SQLAlchemy Query object that represents the data this view
        will display.

        See `Django's SingleObjectMixin.get_queryset`_.


Multiple object mixins
----------------------

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

    .. method:: get_query_object()

        Returns the SQLAlchemy Query object that represents the data this view
        will display.

        See `Django's MultipleObjectMixin.get_queryset`_.

    .. method:: paginate_query_object(query_object, page_size)

        Returns a 4-tuple containing (paginator, page, object_list,
        is_paginated).
        
        See `Django's MultipleObjectMixin.paginate_queryset`_.

    .. method:: get_paginate_by(query_object)

        Returns the number of items to paginate by, or None for no pagination.

        See `Django's MultipleObjectMixin.get_paginate_by`_.

    .. method:: get_paginator(query_object, per_page, orphans=0, allow_empty_first_page=True)

        See `Django's MultipleObjectMixin.get_paginator`_.

    .. method:: get_context_object_name(object_list)

        Returns the context variable name that will be used to contain the
        list of data that this view is manipulating. If object_list is a
        SQLAlchemy Query object, it'll somehow find the name of the model.


.. _Django: http://djangoproject.com
.. _Django's Documentation: http://docs.djangoproject.com/en/1.4/

.. _Django's SingleObjectMixin.queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.SingleObjectMixin.queryset
.. _Django's SingleObjectMixin.get_queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.detail.SingleObjectMixin.get_queryset

.. _Django's MultipleObjectMixin.queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.queryset
.. _Django's MultipleObjectMixin.get_queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.get_queryset
.. _Django's MultipleObjectMixin.paginate_queryset: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.paginate_queryset
.. _Django's MultipleObjectMixin.get_paginate_by: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.get_paginate_by
.. _Django's MultipleObjectMixin.get_paginator: https://docs.djangoproject.com/en/1.4/ref/class-based-views/#django.views.generic.list.MultipleObjectMixin.get_paginator
