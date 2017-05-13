# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from django.conf import settings
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property

from django_busybody.custom_storages import ChainStorage


class TestStorageA(FileSystemStorage):
    TEST_LOCATION = '/tmp/django_busybody_test_storage_a'

    @cached_property
    def location(self):
        return self.TEST_LOCATION


class TestStorageB(TestStorageA):
    TEST_LOCATION = '/tmp/django_busybody_test_storage_b'


class TestDjango_storages_chain(TestCase):

    def setUp(self):
        settings.CHAIN_STORAGES = ['tests.test_storages.TestStorageA', 'tests.test_storages.TestStorageB']
        self.storage = ChainStorage()
        self.storage_a = TestStorageA()
        self.storage_b = TestStorageB()
        self.storage_x = ChainStorage(TestStorageA, TestStorageB)

    def tearDown(self):
        pass

    def test_create_and_access(self):
        key = self.storage.save('hello.txt', ContentFile('hello world'))
        key_a = self.storage_a.save('hello2.txt', ContentFile('hello world'))
        key_b = self.storage_b.save('hello3.txt', ContentFile('hello world'))

        self.assertTrue(self.storage.exists(key))
        self.assertTrue(self.storage.exists(key_a))
        self.assertTrue(self.storage.exists(key_b))

        self.assertTrue(self.storage_a.exists(key))
        self.assertTrue(self.storage_a.exists(key_a))
        self.assertFalse(self.storage_a.exists(key_b))

        self.assertFalse(self.storage_b.exists(key))
        self.assertFalse(self.storage_b.exists(key_a))
        self.assertTrue(self.storage_b.exists(key_b))

    def test_delete(self):
        key = self.storage.save('hello.txt', ContentFile('hello world'))
        key_a = self.storage_a.save('hello2.txt', ContentFile('hello world'))
        key_b = self.storage_b.save('hello3.txt', ContentFile('hello world'))
        self.storage.delete(key)
        self.storage.delete(key_a)
        self.storage.delete(key_b)
        self.assertFalse(self.storage.exists(key))
        self.assertFalse(self.storage.exists(key_a))
        self.assertTrue(self.storage.exists(key_b))

    def test_api(self):
        key = self.storage.save('hello.txt', ContentFile('hello world'))
        self.assertEqual(self.storage.open(key, 'rb').read(), b'hello world')

        self.storage.get_valid_name(key)
        self.storage.get_available_name(key)
        self.storage.generate_filename(key)
        self.storage.path(key)
        self.storage.listdir('')
        self.storage.size(key)
        self.storage.url(key)
        self.storage.accessed_time(key)
        self.storage.created_time(key)
        self.storage.modified_time(key)
        self.storage.get_accessed_time(key)
        self.storage.get_created_time(key)
        self.storage.get_modified_time(key)