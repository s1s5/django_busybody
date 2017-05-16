# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os
import time
import shutil
import copy

# from six import binary_type

from django.test import TestCase
from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from django.utils.functional import cached_property
from django.core.management import call_command
from django.contrib.staticfiles.storage import StaticFilesStorage

from django_busybody.custom_storages import (
    CachedHashValueFilesMixin,
    CachedManifestFilesMixin
)


class StatisticsMixin(object):
    _save_count = {}
    _open_count = {}

    def _save(self, name, *args, **kwargs):
        self._save_count[name] = self._save_count.get(name, 0) + 1
        return super(StatisticsMixin, self)._save(name, *args, **kwargs)

    def open(self, name, *args, **kwargs):
        self._open_count[name] = self._open_count.get(name, 0) + 1
        return super(StatisticsMixin, self).open(name, *args, **kwargs)


class TestStorageA(CachedHashValueFilesMixin, StatisticsMixin,
                   StaticFilesStorage):
    pass


class TestStorageB(CachedManifestFilesMixin, StatisticsMixin,
                   StaticFilesStorage):
    pass


class StorageTestMixin(object):

    def setUp(self):
        super(StorageTestMixin, self).setUp()
        self.org_static_root = settings.STATIC_ROOT
        self.org_static_url = settings.STATIC_URL
        self.org_staticfiles_dirs = settings.STATICFILES_DIRS
        self.org_installed_apps = copy.copy(settings.INSTALLED_APPS)
        self.org_storage_name = settings.STATICFILES_STORAGE
        settings.INSTALLED_APPS.remove('django.contrib.admin')
        settings.STATIC_ROOT = 'django_busybody_test_static_root'
        settings.STATIC_URL = '/static/'
        settings.STATICFILES_DIRS = ['django_busybody_test_static_files_dir']
        settings.STATICFILES_STORAGE_TEST = self.storage_name
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

        if os.path.exists(settings.STATICFILES_DIRS[0]):
            shutil.rmtree(settings.STATICFILES_DIRS[0])
        os.mkdir(settings.STATICFILES_DIRS[0])

        StatisticsMixin._save_count = {}
        StatisticsMixin._open_count = {}

    def tearDown(self):
        super(StorageTestMixin, self).tearDown()
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

        if os.path.exists(settings.STATICFILES_DIRS[0]):
            shutil.rmtree(settings.STATICFILES_DIRS[0])

        settings.INSTALLED_APPS = self.org_installed_apps
        settings.STATIC_ROOT = self.org_static_root
        settings.STATIC_URL = self.org_static_url
        settings.STATICFILES_DIRS = self.org_staticfiles_dirs
        settings.STATICFILES_STORAGE = self.org_storage_name

    def call_command(self):
        kwargs = {
            'interactive': False,
            'verbosity': 0,
            'ignore_patterns': ['admin*'],
        }
        call_command('collectstatic', **kwargs)
        from django.contrib.staticfiles.storage import staticfiles_storage
        staticfiles_storage.reset_storage()


class TestDjango_busybody_cached(StorageTestMixin, TestCase):
    storage_name = 'tests.test_commands.TestStorageA'

    def test_command_cached(self):
        save_count = StatisticsMixin._save_count
        filename = os.path.join(settings.STATICFILES_DIRS[0], 'test')
        contents = 'hello world'
        with open(filename, 'w') as fp:
            fp.write(contents)
        self.call_command()
        self.assertEqual(save_count['test'], 1)

        os.utime(filename, (time.time() + 600, time.time() + 600))
        self.call_command()
        self.assertEqual(save_count['test'], 1)

        with open(filename, 'w') as fp:
            fp.write(contents + '1')
        os.utime(filename, (time.time() + 600, time.time() + 600))
        self.call_command()
        self.assertEqual(save_count['test'], 2)


class TestDjango_busybody_manifest(StorageTestMixin, TestCase):
    storage_name = 'tests.test_commands.TestStorageB'

    def test_command_manifest(self):
        save_count = StatisticsMixin._save_count
        filename = os.path.join(settings.STATICFILES_DIRS[0], 'test')
        contents = 'hello world'
        with open(filename, 'w') as fp:
            fp.write(contents)
        self.call_command()
        self.assertEqual(save_count['test'], 1)

        os.utime(filename, (time.time() + 600, time.time() + 600))
        self.call_command()
        self.assertEqual(save_count['test'], 1)

        with open(filename, 'w') as fp:
            fp.write(contents + '1')
        os.utime(filename, (time.time() + 600, time.time() + 600))
        self.call_command()
        self.assertEqual(save_count['test'], 2)
        for i in save_count:
            if i.startswith('test.'):
                self.assertEqual(save_count[i], 1)

    def test_command_manifest_css(self):
        save_count = StatisticsMixin._save_count
        filename_css = os.path.join(settings.STATICFILES_DIRS[0], 'test.css')
        filename_img = os.path.join(settings.STATICFILES_DIRS[0], 'img')
        contents = 'url("./img")'
        with open(filename_css, 'w') as fp:
            fp.write(contents)
        with open(filename_img, 'w') as fp:
            fp.write("hello world")
        self.call_command()
        self.assertEqual(save_count['test.css'], 1)
        self.assertEqual(save_count['img'], 1)

        os.utime(filename_css, (time.time() + 600, time.time() + 600))
        os.utime(filename_img, (time.time() + 600, time.time() + 600))
        self.call_command()
        self.assertEqual(save_count['test.css'], 1)
        self.assertEqual(save_count['img'], 1)

        with open(filename_img, 'w') as fp:
            fp.write('hello world second time')
        os.utime(filename_css, (time.time() + 600, time.time() + 600))
        os.utime(filename_img, (time.time() + 600, time.time() + 600))
        self.call_command()
        # self.assertEqual(save_count['test.css'], 2)
        self.assertEqual(save_count['img'], 2)
        # print(save_count)
