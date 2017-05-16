# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from django.conf import settings
from django.utils.module_loading import import_string


class TestStaticStorage(object):
    def __init__(self, *args, **kwargs):
        self.__dict__['args_'] = args
        self.__dict__['kwargs_'] = kwargs
        self.__dict__['storages_'] = {}

    def reset_storage(self):
        cur_key = settings.STATICFILES_STORAGE_TEST
        self.__dict__['storages_'].pop(cur_key)

    def __getattr__(self, key):
        cur_key = settings.STATICFILES_STORAGE_TEST
        storage = self.__dict__['storages_'].get(cur_key)
        if storage is None:
            Storage = import_string(cur_key)
            storage = Storage(*self.__dict__['args_'], **self.__dict__['kwargs_'])
            self.__dict__['storages_'][cur_key] = storage
        return getattr(storage, key)
