#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_busybody
------------

Tests for `django_busybody` models module.
"""
from __future__ import unicode_literals
from django.test import TestCase

from . import models
from django.contrib.contenttypes.models import ContentType
import django_busybody.models as bb_models
from django_busybody import easy_crypto


class TestDjango_busybody(TestCase):

    def setUp(self):
        self.obj = models.EncryptTest.objects.create(
            without_encrypt='1',
            with_encrypt='1',
            without_encrypt_with_log='1',
            with_encrypt_with_log='1')

    def test_get(self):
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        self.assertEqual(obj.without_encrypt, '1')
        self.assertEqual(obj.with_encrypt, '1')
        self.assertEqual(obj.without_encrypt_with_log, '1')
        self.assertEqual(obj.with_encrypt_with_log, '1')

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

    def tearDown(self):
        models.EncryptTest.objects.get(pk=self.obj.pk).delete()


class TestDjango_history(TestCase):

    def setUp(self):
        self.obj = models.EncryptTest.objects.create(
            without_encrypt='1',
            with_encrypt='1',
            without_encrypt_with_log='1',
            with_encrypt_with_log='1')

    def tearDown(self):
        models.EncryptTest.objects.get(pk=self.obj.pk).delete()

    def test_history(self):
        obj = models.EncryptTest.objects.get(pk=self.obj.pk)
        obj.without_encrypt_with_log = '2'
        obj.save()
        history = bb_models.History.objects.filter(
            target_type=ContentType.objects.get_for_model(models.EncryptTest),
            target_object_id=obj.pk).order_by('changed_at')
        # TOOD: ちゃんとログ取れてるかチェック


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
