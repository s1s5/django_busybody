#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_busybody
------------

Tests for `django_busybody` models module.
"""
from __future__ import unicode_literals

import datetime
import json
import uuid
from mock import patch

from django.test import TestCase
# from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.utils import timezone

import django_busybody.models as bb_models
from django_busybody import easy_crypto
from django_busybody.middlewares import GlobalRequestMiddleware

from . import models


class TestDjango_busybody(TestCase):

    def setUp(self):
        self.obj = models.EncryptTest.objects.create(
            without_encrypt='1',
            with_encrypt='1',
            without_encrypt_with_log='1',
            with_encrypt_with_log='1')

    def test_get(self):
        print("=" * 120)
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        print("=" * 80)
        self.assertEqual(obj.without_encrypt, '1')
        self.assertEqual(obj.with_encrypt, '1')
        self.assertEqual(obj.without_encrypt_with_log, '1')
        self.assertEqual(obj.with_encrypt_with_log, '1')

    def test_get_and_save(self):
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        self.assertEqual(obj.without_encrypt, '1')
        self.assertEqual(obj.with_encrypt, '1')
        self.assertEqual(obj.without_encrypt_with_log, '1')
        self.assertEqual(obj.with_encrypt_with_log, '1')
        obj.save()
        self.assertEqual(obj.without_encrypt, '1')
        self.assertEqual(obj.with_encrypt, '1')
        self.assertEqual(obj.without_encrypt_with_log, '1')
        self.assertEqual(obj.with_encrypt_with_log, '1')
        self.assertEqual(models.EncryptTest.objects.filter(without_encrypt__exact='1').count(), 1)
        self.assertEqual(models.EncryptTest.objects.filter(with_encrypt__exact='1').count(), 0)
        self.assertEqual(models.EncryptTest.objects.filter(without_encrypt_with_log__exact='1').count(), 1)
        self.assertEqual(models.EncryptTest.objects.filter(with_encrypt_with_log__exact='1').count(), 0)

    def test_encrypt(self):
        self.assertEqual(models.EncryptTest.objects.filter(without_encrypt__exact='1').count(), 1)
        self.assertEqual(models.EncryptTest.objects.filter(with_encrypt__exact='1').count(), 0)
        self.assertEqual(models.EncryptTest.objects.filter(without_encrypt_with_log__exact='1').count(), 1)
        self.assertEqual(models.EncryptTest.objects.filter(with_encrypt_with_log__exact='1').count(), 0)

    def test_unicode(self):
        obj = models.EncryptTest.objects.create(
            without_encrypt='日本語',
            with_encrypt='日本語',
            without_encrypt_with_log='日本語',
            with_encrypt_with_log='日本語')
        obj = models.EncryptTest.objects.get(pk=obj.pk)

        self.assertEqual(obj.without_encrypt, '日本語')
        self.assertEqual(obj.with_encrypt, '日本語')
        self.assertEqual(obj.without_encrypt_with_log, '日本語')
        self.assertEqual(obj.with_encrypt_with_log, '日本語')

    def test_invalid_decrypt(self):
        models.EncryptTest.objects.filter(pk=self.obj.pk).update(with_encrypt='no_encrypt')
        self.assertEqual(models.EncryptTest.objects.filter(with_encrypt__exact='no_encrypt').count(), 1)
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        self.assertEqual(obj.with_encrypt, 'no_encrypt')

    def test_invalid_decrypt2(self):
        models.EncryptTest.objects.filter(pk=self.obj.pk).update(with_encrypt='日本語')
        self.assertEqual(models.EncryptTest.objects.filter(with_encrypt__exact='日本語').count(), 1)
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        self.assertEqual(obj.with_encrypt, '日本語')

    def test_invalid_decrypt3(self):
        import base64
        from Crypto.Cipher import AES
        iv = b'\xf2\xae' * 8
        raw = '日本語' * 16
        cipher = AES.new(easy_crypto._cipher.key, AES.MODE_CBC, iv)
        value = base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))
        models.EncryptTest.objects.filter(pk=self.obj.pk).update(with_encrypt=value)
        models.EncryptTest.objects.get(pk=self.obj.pk)

    def tearDown(self):
        models.EncryptTest.objects.get(pk=self.obj.pk).delete()


class TestDjango_history(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        self.obj = models.AllField.objects.create(
            big_integer=0,
            binary=b"",
            boolean=True,
            char="",
            date=timezone.now(),
            date_time=timezone.now(),
            decimal=0,
            duration=datetime.timedelta(seconds=1),
            email="hoge@email.com",
            _file=default_storage.save("hello.txt", ContentFile("hello world")),
            file_path="hoge.txt",
            _float=0.0,
            integer=0,
            generic_ip_address="0.0.0.0",
            null_boolean=None,
            positive_integer=1,
            positive_small_integer=1,
            slug="slug",
            small_integer=0,
            text="text",
            time=timezone.now(),
            url="http://hoge.com",
            uuid=uuid.uuid4().hex,
            foreign_key=self.user,
            one_to_one=self.user)

    @property
    def latest_history(self):
        return bb_models.History.objects.all().order_by('-changed_at')[0]

    def test_history_bool(self):
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj.boolean = False
        obj.null_boolean = True
        obj.save()

    def test_history_integer(self):
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj.big_integer = 0
        obj.decimal = 0
        obj._float = 0.0
        obj.integer = 0
        obj.positive_integer = 1
        obj.positive_small_integer = 1
        obj.small_integer = 0
        obj.save()

    def test_history_binary(self):
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj.binary = b"binary_value"
        obj.save()

    def test_history_string(self):
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj.char = "char"
        obj.email = "hoge2@email.com"
        obj.file_path = "hoge2.txt"
        obj.generic_ip_address = "0.0.0.1"
        obj.slug = "slug1"
        obj.text = "text1"
        obj.url = "http://hoge1.com"
        obj.uuid = uuid.uuid4().hex
        obj.save()

    def test_history_datetime(self):
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj.date = timezone.now()
        obj.date_time = timezone.now()
        obj.duration = datetime.timedelta(seconds=2)
        obj.time = timezone.now()
        obj.save()

    def test_history_file(self):
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj._file.save("hello2.txt",
                       ContentFile("hello world2"), save=True)

    def test_history_key(self):
        new_user = get_user_model().objects.create(username='test2')
        obj = models.AllField.objects.get(pk=self.obj.pk)
        obj.foreign_key = new_user
        obj.one_to_one = new_user
        obj.save()


class TestDjango_history_encrypt(TestCase):

    def setUp(self):
        self.obj = models.EncryptTest.objects.create(
            without_encrypt='1',
            with_encrypt='1',
            without_encrypt_with_log='1',
            with_encrypt_with_log='1')

    def tearDown(self):
        models.EncryptTest.objects.get(pk=self.obj.pk).delete()

    def check_history(self, obj, key='without_encrypt_with_log'):
        history = bb_models.History.objects.filter(
            target_type=ContentType.objects.get_for_model(models.EncryptTest),
            target_object_id=obj.pk).order_by('-changed_at')[0]
        j = json.loads(history.changes)
        self.assertEqual(eval(j[key][0]), "1")
        self.assertEqual(eval(j[key][1]), "2")
        return history

    def test_history(self):
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        obj.without_encrypt_with_log = '2'
        obj.save()
        history = self.check_history(obj)
        self.assertEqual(history.target, obj)

    def test_history_encrypted(self):
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        obj.with_encrypt_with_log = '2'
        obj.save()
        history = self.check_history(obj, 'with_encrypt_with_log')
        self.assertEqual(history.target, obj)

    def test_history_with_request(self):
        request = RequestFactory().get('/customer/details')
        GlobalRequestMiddleware.thread_local.request = request
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        obj.without_encrypt_with_log = '2'
        obj.save()
        self.check_history(obj)

    def test_history_with_request_user(self):
        request = RequestFactory().get('/customer/details')
        request.user = get_user_model().objects.create(username='test')
        GlobalRequestMiddleware.thread_local.request = request
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        obj.without_encrypt_with_log = '2'
        obj.save()
        history = self.check_history(obj)
        self.assertEqual(history.who, request.user)

    def test_history_without_request(self):
        if hasattr(GlobalRequestMiddleware.thread_local, 'request'):
            delattr(GlobalRequestMiddleware.thread_local, 'request')
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        obj.without_encrypt_with_log = '2'
        obj.save()
        self.check_history(obj)


class TestDjango_encrypt(TestCase):

    def setUp(self):
        self.cipher0 = easy_crypto.AESCipher('key' * 32)
        self.cipher1 = easy_crypto.AESCipher('key')

    def test_encrypt(self):
        values = [
            b'binary',
            'ascii',
            1,
            [1, 'str'],
            [1, '日本語'],
        ]
        for cipher in [self.cipher0, self.cipher1]:
            for value in values:
                encrypted = cipher.encrypt(value)
                decrypted = cipher.decrypt(encrypted)
                self.assertEqual(value, decrypted)


class MyTime(object):
    def time(self):
        return self.time


my_time = MyTime()


class NaiveLockTest(TestCase):
    def test_lock_work(self):
        bb_models.NaiveLock.acquire('test')

    def test_lock_work_with(self):
        with bb_models.NaiveLock.acquire('test'):
            pass

    def test_lock_failure(self):
        with bb_models.NaiveLock.acquire('test'):
            try:
                bb_models.NaiveLock.acquire('test')
            except bb_models.LockError:
                pass
            else:
                self.assertFalse(True)

    @patch('django_busybody.models.NaiveLock.get_current_time', my_time.time)
    def test_lock_timeout(self):
        my_time.time = 0
        with bb_models.NaiveLock.acquire('test', timeout=100):
            my_time.time = 1000
            bb_models.NaiveLock.acquire('test')
