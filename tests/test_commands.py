# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os
# import time
import shutil
import copy

# from six import binary_type

from django.test import TestCase
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from django.utils.functional import cached_property
from django.core.management import call_command

from django_busybody.custom_storages import (
    CachedHashValueFilesMixin,
    CachedManifestFilesMixin
)


class StatisticsMixin(object):
    _save_count = {}

    def _save(self, name, *args, **kwargs):
        self._save_count[name] = self._save_count.get(name, 0) + 1
        return super(StatisticsMixin, self)._save(name, *args, **kwargs)


class TestStorageA(CachedHashValueFilesMixin, StatisticsMixin,
                   FileSystemStorage):
    pass


class TestStorageB(CachedManifestFilesMixin, StatisticsMixin,
                   FileSystemStorage):
    pass


class TestDjango_busybody_collectstatic(TestCase):

    def setUp(self):
        self.org_static_root = settings.STATIC_ROOT
        self.org_static_url = settings.STATIC_URL
        self.org_staticfiles_dirs = settings.STATICFILES_DIRS
        self.org_installed_apps = copy.copy(settings.INSTALLED_APPS)
        settings.INSTALLED_APPS.remove('django.contrib.admin')
        settings.STATIC_ROOT = 'django_busybody_test_static_root'
        settings.STATIC_URL = '/static/'
        settings.STATICFILES_DIRS = ['django_busybody_test_static_files_dir']
        settings.STATICFILES_STORAGE = 'tests.test_commands.TestStorageA'
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

        if os.path.exists(settings.STATICFILES_DIRS[0]):
            shutil.rmtree(settings.STATICFILES_DIRS[0])
        os.mkdir(settings.STATICFILES_DIRS[0])

    def test_command_base(self):
        kwargs = {
            'interactive': False,
            'verbosity': 0,
            'ignore_patterns': ['admin*'],
        }
        filename = os.path.join(settings.STATICFILES_DIRS[0], 'test')
        dst_filename = os.path.join(settings.STATIC_ROOT, 'test')
        contents = 'hello world'
        with open(filename, 'w') as fp:
            fp.write(contents)
        call_command('collectstatic', **kwargs)

        print(StatisticsMixin._save_count)
    #     self.assertTrue(os.path.exists(dst_filename))
    #     self.assertEqual(time.ctime(os.path.getmtime(dst_filename)), when_modified)
    #     # print("last modified: {}".format(time.ctime(os.path.getmtime(dst_filename))))
    #     # print("created: {}".format(time.ctime(os.path.getctime(dst_filename))))

    #     os.utime(filename, (time.time() + 600, time.time() + 600))
    #     call_command('collectstatic_ext', **kwargs)
    #     self.assertTrue(os.path.exists(dst_filename))
    #     # TODO:タイミングによっては失敗する。。
    #     self.assertEqual(time.ctime(os.path.getmtime(dst_filename)), when_modified)
    #     time.sleep(1)
    #     with open(filename, 'w') as fp:
    #         fp.write(contents + '1')
    #     os.utime(filename, (time.time() + 600, time.time() + 600))
    #     call_command('collectstatic_ext', **kwargs)
    #     self.assertTrue(os.path.exists(dst_filename))
    #     self.assertNotEqual(time.ctime(os.path.getmtime(dst_filename)), when_modified)

    # def test_command_contents(self):
    #     verbosity = 0
    #     contents_list = ['hello world', '日本語', b'hogehoge']
    #     files = []
    #     for index, contents in enumerate(contents_list):
    #         filename = os.path.join(settings.STATICFILES_DIRS[0], 'test{}'.format(index))
    #         dst_filename = os.path.join(settings.STATIC_ROOT, 'test{}'.format(index))
    #         if isinstance(contents, binary_type):
    #             with open(filename, 'wb') as fp:
    #                 fp.write(contents)
    #         else:
    #             with open(filename, 'wb') as fp:
    #                 fp.write(contents.encode('UTF-8'))
    #         files.append((filename, dst_filename))

    #     call_command('collectstatic_ext', interactive=False, verbosity=verbosity)
    #     for _, dst_filename in files:
    #         self.assertTrue(os.path.exists(dst_filename))

    # def test_command_dryrun(self):
    #     verbosity = 0
    #     contents_list = ['hello world', '日本語', b'hogehoge']
    #     files = []
    #     for index, contents in enumerate(contents_list):
    #         filename = os.path.join(settings.STATICFILES_DIRS[0], 'test{}'.format(index))
    #         dst_filename = os.path.join(settings.STATIC_ROOT, 'test{}'.format(index))
    #         if isinstance(contents, binary_type):
    #             with open(filename, 'wb') as fp:
    #                 fp.write(contents)
    #         else:
    #             with open(filename, 'wb') as fp:
    #                 fp.write(contents.encode('UTF-8'))
    #         files.append((filename, dst_filename))

    #     call_command('collectstatic_ext', interactive=False, dry_run=True, verbosity=verbosity)
    #     for _, dst_filename in files:
    #         self.assertFalse(os.path.exists(dst_filename))

    def tearDown(self):
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

        if os.path.exists(settings.STATICFILES_DIRS[0]):
            shutil.rmtree(settings.STATICFILES_DIRS[0])

        settings.INSTALLED_APPS = self.org_installed_apps
        settings.STATIC_ROOT = self.org_static_root
        settings.STATIC_URL = self.org_static_url
        settings.STATICFILES_DIRS = self.org_staticfiles_dirs
