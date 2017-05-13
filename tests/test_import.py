# coding: utf-8

from django.test import TestCase


class TestDjango_busybody(TestCase):

    def setUp(self):
        pass

    def test_import_busybody(self):
        from django_busybody import apps
        apps

    def test_import_storage(self):
        from django_busybody import custom_storages
        custom_storages
        custom_storages.ChainStorage
        custom_storages.StaticS3Storage
        custom_storages.ManifestFilesStaticS3Storage
        custom_storages.MediaS3Storage

    def test_import_backend(self):
        from django_busybody import custom_backends
        custom_backends.LogEmailBackend
