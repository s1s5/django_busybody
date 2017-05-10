=====
Usage
=====

To use django_busybody in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_busybody.apps.DjangoBusybodyConfig',
        ...
    )

Add django_busybody's URL patterns:

.. code-block:: python

    from django_busybody import urls as django_busybody_urls


    urlpatterns = [
        ...
        url(r'^', include(django_busybody_urls)),
        ...
    ]
