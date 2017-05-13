# coding: utf-8
from django.conf import settings

try:
    from storages.backends.s3boto import S3BotoStorage
    from django.contrib.staticfiles.storage import ManifestFilesMixin

    class StaticS3Storage(S3BotoStorage):
        location = getattr(settings, 'STATICFILES_LOCATION',
                           '{}/{}'.format(getattr(settings, 'PROJECT_NAME', 'django'), 'static'))

    class ManifestFilesStaticS3Storage(ManifestFilesMixin, S3BotoStorage):
        location = getattr(settings, 'STATICFILES_LOCATION',
                           '{}/{}'.format(getattr(settings, 'PROJECT_NAME', 'django'), 'static'))

    class MediaS3Storage(S3BotoStorage):
        location = getattr(settings, 'MEDIAFILES_LOCATION',
                           '{}/{}'.format(getattr(settings, 'PROJECT_NAME', 'django'), 'media'))

except ImportError:
    pass
