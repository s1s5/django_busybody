# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import os
import time
import shutil

from six import binary_type

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command


class TestDjango_busybody_collectstatic(TestCase):

    def setUp(self):
        self.org_static_root = settings.STATIC_ROOT
        self.org_static_url = settings.STATIC_URL
        self.org_staticfiles_dirs = settings.STATICFILES_DIRS
        settings.STATIC_ROOT = 'django_busybody_test_static_root'
        settings.STATIC_URL = '/static/'
        settings.STATICFILES_DIRS = ['django_busybody_test_static_files_dir']
        if not os.path.exists(settings.STATICFILES_DIRS[0]):
            os.mkdir(settings.STATICFILES_DIRS[0])

    def test_command_base(self):
        verbosity = 0
        filename = os.path.join(settings.STATICFILES_DIRS[0], 'test')
        dst_filename = os.path.join(settings.STATIC_ROOT, 'test')
        contents = 'hello world'
        with open(filename, 'w') as fp:
            fp.write(contents)
        when_modified = time.ctime(os.path.getmtime(filename))
        call_command('collectstatic_ext', interactive=False, verbosity=verbosity)
        self.assertTrue(os.path.exists(dst_filename))
        self.assertEqual(time.ctime(os.path.getmtime(dst_filename)), when_modified)
        # print("last modified: {}".format(time.ctime(os.path.getmtime(dst_filename))))
        # print("created: {}".format(time.ctime(os.path.getctime(dst_filename))))

        os.utime(filename, (time.time() + 600, time.time() + 600))
        call_command('collectstatic_ext', interactive=False, verbosity=verbosity)
        self.assertTrue(os.path.exists(dst_filename))
        self.assertEqual(time.ctime(os.path.getmtime(dst_filename)), when_modified)

        time.sleep(1)
        with open(filename, 'w') as fp:
            fp.write(contents + '1')
        os.utime(filename, (time.time() + 600, time.time() + 600))
        call_command('collectstatic_ext', interactive=False, verbosity=verbosity)
        self.assertTrue(os.path.exists(dst_filename))
        self.assertNotEqual(time.ctime(os.path.getmtime(dst_filename)), when_modified)

    def test_command_contents(self):
        verbosity = 0
        contents_list = ['hello world', '日本語', b'hogehoge']
        files = []
        for index, contents in enumerate(contents_list):
            filename = os.path.join(settings.STATICFILES_DIRS[0], 'test{}'.format(index))
            dst_filename = os.path.join(settings.STATIC_ROOT, 'test{}'.format(index))
            if isinstance(contents, binary_type):
                with open(filename, 'wb') as fp:
                    fp.write(contents)
            else:
                with open(filename, 'wb') as fp:
                    fp.write(contents.encode('UTF-8'))
            files.append((filename, dst_filename))

        call_command('collectstatic_ext', interactive=False, verbosity=verbosity)
        for _, dst_filename in files:
            self.assertTrue(os.path.exists(dst_filename))

    def tearDown(self):
        settings.STATIC_ROOT = self.org_static_root
        settings.STATIC_URL = self.org_static_url
        settings.STATICFILES_DIRS = self.org_staticfiles_dirs
