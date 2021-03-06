# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import binascii

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import pre_save, post_save, post_init

from . import easy_crypto
from . import models

__global_reference = []


class Encryptor(object):
    def __init__(self, fields):
        self.fields = fields

    def encrypt(self, sender, instance, **kwargs):
        for field in self.fields:
            setattr(instance, field, easy_crypto.aes_encrypt(getattr(instance, field)))

    def decrypt(self, sender, instance, **kwargs):
        if not instance.pk:
            return
        for field in self.fields:
            try:
                # if isinstance(getattr(instance, field), str):
                #     v = getattr(instance, field)
                #     if v[0] == "b" and v[1] == "'" and v[-1] == "'":
                #         setattr(instance, field, v[2:-1].encode('ascii'))
                setattr(instance, '{}_encrypted'.format(field), getattr(instance, field))
                setattr(instance, field, easy_crypto.aes_decrypt(getattr(instance, field)))
            except (ValueError, binascii.Error):
                setattr(instance, '{}_encrypted'.format(field),
                        easy_crypto.aes_encrypt(getattr(instance, field)))


class History(object):
    def __init__(self, target_klass, includes, excludes, need_to_save):
        self.target_klass = target_klass
        self.includes = includes
        self.excludes = excludes
        self.need_to_save = need_to_save

    def on_change(self, *args, **kwargs):
        models.History._on_change(self.includes, self.excludes, self.need_to_save, *args, **kwargs)

    def on_create(self, *args, **kwargs):
        models.History._on_create(self.includes, self.excludes, self.need_to_save, *args, **kwargs)


def encrypt_field(klass, field_name):
    encrypt_fields(klass, [field_name])


def encrypt_fields(klass, field_names):
    if not getattr(settings, 'CRYPTO_KEY', None):  # pragma: no cover
        raise ImproperlyConfigured('CRYPTO_KEY is not set in settings')
    cb_ins = Encryptor(field_names)
    __global_reference.append(cb_ins)
    pre_save.connect(cb_ins.encrypt, klass)
    post_save.connect(cb_ins.decrypt, klass)
    post_init.connect(cb_ins.decrypt, klass)


def save_history(klass, includes=None, excludes=None, need_to_save=None):
    cb_ins = History(klass, includes, excludes, need_to_save)
    __global_reference.append(cb_ins)
    pre_save.connect(cb_ins.on_change, klass)
    post_save.connect(cb_ins.on_create, klass)
