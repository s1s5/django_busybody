# coding: utf-8
from __future__ import absolute_import

from django.conf import settings
from django.utils.module_loading import import_string


class ChainStorage(object):
    def __init__(self, *chains):
        if not chains:
            chains = map(import_string, settings.CHAIN_STORAGES)
        self.chains = [x() for x in chains]

    def __callExists(self, name, attr, args=(), kw={}):
        for chain in self.chains:
            if chain.exists(name):
                return getattr(chain, attr)(*args, **kw)
        return getattr(self.chains[0], attr)(*args, **kw)  # cause error

    def open(self, name, mode='rb'):
        return self.__callExists(name, 'open', (name, mode))

    def save(self, name, content, max_length=None):
        return self.chains[0].save(name, content, max_length)

    def get_valid_name(self, name):
        return self.chains[0].get_valid_name(name)

    def get_available_name(self, name, max_length=None):
        return self.chains[0].get_available_name(name, max_length)

    def generate_filename(self, filename):
        return self.chains[0].generate_filename(filename)

    def path(self, name):
        return self.__callExists(name, 'path', (name, ))

    def delete(self, name):
        return self.chains[0].delete(name)

    def exists(self, name):
        return self.__callExists(name, 'exists', (name, ))

    def listdir(self, path):
        return self.__callExists(path, 'listdir', (path, ))

    def size(self, name):
        return self.__callExists(name, 'size', (name, ))

    def url(self, name):
        return self.__callExists(name, 'url', (name, ))

    def accessed_time(self, name):
        return self.__callExists(name, 'accessed_time', (name, ))

    def created_time(self, name):
        return self.__callExists(name, 'created_time', (name, ))

    def modified_time(self, name):
        return self.__callExists(name, 'modified_time', (name, ))

    def get_accessed_time(self, name):
        return self.__callExists(name, 'get_accessed_time', (name, ))

    def get_created_time(self, name):
        return self.__callExists(name, 'get_created_time', (name, ))

    def get_modified_time(self, name):
        return self.__callExists(name, 'get_modified_time', (name, ))
