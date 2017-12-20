# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import hashlib

from django.conf import settings
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property

from django_busybody.custom_storages import ChainStorage
from django_busybody.custom_storages import HashedFileSystemStorage

import django


class TestStorageMixin(object):
    @cached_property
    def location(self):
        return self.TEST_LOCATION


class TestStorageA(TestStorageMixin, FileSystemStorage):
    TEST_LOCATION = 'django_busybody_test_storage_a'


class TestStorageB(TestStorageMixin, FileSystemStorage):
    TEST_LOCATION = 'django_busybody_test_storage_b'


class TestHashedStorage(TestStorageMixin, HashedFileSystemStorage):
    TEST_LOCATION = 'django_busybody_test_storage_hashed'


class TestDjango_storages_chain(TestCase):

    def setUp(self):
        settings.CHAIN_STORAGES = ['tests.test_storages.TestStorageA', 'tests.test_storages.TestStorageB']
        self.storage = ChainStorage()
        self.storage_a = TestStorageA()
        self.storage_b = TestStorageB()
        self.storage_x = ChainStorage(TestStorageA, TestStorageB)

        # create directories at first
        self.storage_a.save('x.txt', ContentFile('hello world'))
        self.storage_b.save('x.txt', ContentFile('hello world'))

    def tearDown(self):
        if os.path.exists(self.storage_a.location):
            shutil.rmtree(self.storage_a.location)
        if os.path.exists(self.storage_b.location):
            shutil.rmtree(self.storage_b.location)

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
        if django.VERSION[0] == 1:
            self.storage.accessed_time(key)
            self.storage.created_time(key)
            self.storage.modified_time(key)
        self.storage.get_accessed_time(key)
        self.storage.get_created_time(key)
        self.storage.get_modified_time(key)


class TestDjango_storages_hashed(TestCase):

    def setUp(self):
        self.storage = TestHashedStorage()
        if os.path.exists(self.storage.location):
            shutil.rmtree(self.storage.location)
        self.storage.save('empty', ContentFile(''))

    def tearDown(self):
        if os.path.exists(self.storage.location):
            shutil.rmtree(self.storage.location)

    def test_create_and_access(self):
        dirs0, files0 = self.storage.listdir('')
        key = self.storage.save('hello.txt', ContentFile('hello world'))
        expected_key = hashlib.sha1(b'hello world').hexdigest()
        self.assertTrue(expected_key[:2] in key)
        self.assertTrue(expected_key[2:] in key)
        dirs1, files1 = self.storage.listdir('')
        self.storage.save('hellox.txt', ContentFile('hello world'))
        dirs2, files2 = self.storage.listdir('')

        self.assertEqual(len(dirs1) - len(dirs0), 1)
        self.assertEqual(len(dirs2) - len(dirs1), 0)

        dirs3, files3 = self.storage.listdir(list(set(dirs1).difference(dirs0))[0])
        self.assertEqual('{}.txt'.format(expected_key[2:]), files3[0])

    def test_unicode(self):
        self.storage.save('hello.txt', ContentFile('日本語'))
        self.storage.save('日本語.txt', ContentFile('日本語'))
        self.storage.save('日本語.txt', ContentFile(b'binary'))
        self.storage.save(b'binary.txt', ContentFile(b'binary'))
