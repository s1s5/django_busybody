# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from django.conf import settings
from django.test import TestCase
from django.core.mail import EmailMessage
# from django.core.urlresolvers import reverse
from django.core.mail.backends.locmem import EmailBackend


import django_busybody.models as bb_models


class ErrorEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        raise Exception('Some Error Occurred')


class TestDjango_mail_logger(TestCase):

    def setUp(self):
        settings.EMAIL_BACKEND_UPSTREAM = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = 'django_busybody.custom_backends.LogEmailBackend'

    def tearDown(self):
        settings.EMAIL_BACKEND = settings.EMAIL_BACKEND_UPSTREAM

    def test_mail(self):
        mail = EmailMessage('title', 'body', 'from@a.b', ['to@a.b'])
        mail.send()
        # TOOD: ちゃんとログ取れてるかチェック


class TestDjango_mail_logger_error(TestCase):
    def setUp(self):
        self.org_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND_UPSTREAM = 'tests.test_backends.ErrorEmailBackend'
        settings.EMAIL_BACKEND = 'django_busybody.custom_backends.LogEmailBackend'

    def tearDown(self):
        settings.EMAIL_BACKEND = self.org_email_backend

    def test_mail(self):
        mail = EmailMessage('title', 'body', 'from@a.b', ['to@a.b'])
        try:
            mail.send()
        except:
            pass
        else:
            self.assertTrue(False)
