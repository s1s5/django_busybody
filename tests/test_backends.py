# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from django.conf import settings
from django.test import TestCase
from django.core.mail import EmailMessage
from django.utils import timezone
# from django.core.urlresolvers import reverse
from django.core.mail.backends.locmem import EmailBackend
import django_bouncy.models as bouncy_models

import django_busybody.models as bb_models


class ErrorEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        raise Exception('Some Error Occurred')


class TestDjango_mail_logger(TestCase):

    def setUp(self):
        self.org_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND_UPSTREAM = 'django.core.mail.backends.locmem.EmailBackend'
        settings.EMAIL_BACKEND = 'django_busybody.custom_backends.LogEmailBackend'

    def tearDown(self):
        settings.EMAIL_BACKEND = self.org_backend

    def test_mail(self):
        org_len = bb_models.EmailLog.objects.all().count()
        mail = EmailMessage('subject', 'body', 'from@a.b', ['to@a.b'])
        mail.send()
        self.assertEqual(bb_models.EmailLog.objects.all().count() - org_len, 1)
        email_log = bb_models.EmailLog.objects.all().order_by('-pk')[0]
        self.assertEqual(email_log.to, 'to@a.b')
        self.assertEqual(email_log.subject, 'subject')
        self.assertEqual(email_log.body, 'body')

    def test_mail_unicode(self):
        org_len = bb_models.EmailLog.objects.all().count()
        mail = EmailMessage('日本語', '日本語', 'from@a.b', ['to@a.b'])
        mail.send()
        self.assertEqual(bb_models.EmailLog.objects.all().count() - org_len, 1)
        email_log = bb_models.EmailLog.objects.all().order_by('-pk')[0]
        self.assertEqual(email_log.to, 'to@a.b')
        self.assertEqual(email_log.subject, '日本語')
        self.assertEqual(email_log.body, '日本語')


class TestDjango_mail_logger_bouncy(TestCase):

    def setUp(self):
        self.org_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND_UPSTREAM = 'django.core.mail.backends.locmem.EmailBackend'
        settings.EMAIL_BACKEND = 'django_busybody.custom_backends.LogEmailBackend'
        org_len = bb_models.EmailLog.objects.all().count()
        mail = EmailMessage('title', 'body', 'from@a.b', ['to@a.b'])
        mail.extra_headers['message_id'] = 'message_id'
        mail.send()
        self.assertEqual(bb_models.EmailLog.objects.all().count() - org_len, 1)
        self.email_log = bb_models.EmailLog.objects.all().order_by('-pk')[0]

        self.feedback = {
            'sns_topic': 'sns_topic',
            'sns_messageid': 'sns_messageid',
            'mail_timestamp': timezone.now(),
            'mail_id': self.email_log.message_id,
            'mail_from': self.email_log.from_email,
            'address': self.email_log.to,
        }

    def tearDown(self):
        settings.EMAIL_BACKEND = settings.EMAIL_BACKEND

    def test_mail_bounce(self):
        kw = {
            'hard': True,
            'bounce_type': 'bounce_type',
            'bounce_subtype': 'bounce_subtype',
        }
        kw.update(self.feedback)
        bouncy_models.Bounce.objects.create(**kw)
        el = bb_models.EmailLog.objects.get(pk=self.email_log.pk)
        self.assertTrue(el.bounced)
        self.assertFalse(el.complained)
        self.assertFalse(el.delivered)

    def test_mail_complaint(self):
        kw = {
        }
        kw.update(self.feedback)
        bouncy_models.Complaint.objects.create(**kw)
        el = bb_models.EmailLog.objects.get(pk=self.email_log.pk)
        self.assertFalse(el.bounced)
        self.assertTrue(el.complained)
        self.assertFalse(el.delivered)

    def test_mail_delivery(self):
        kw = {
        }
        kw.update(self.feedback)
        bouncy_models.Delivery.objects.create(**kw)
        el = bb_models.EmailLog.objects.get(pk=self.email_log.pk)
        self.assertFalse(el.bounced)
        self.assertFalse(el.complained)
        self.assertTrue(el.delivered)


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
