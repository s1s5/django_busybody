# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import hashlib
import json
from collections import OrderedDict
from six import text_type, binary_type

from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.files.base import ContentFile

from .overwrite import OverwriteStorageMixin


class HashedStorageMixin(object):
    def _save(self, name, content, *args, **kw):
        s = content.read()
        if isinstance(s, text_type):
            s = s.encode('UTF-8', errors='escape')
        if isinstance(name, binary_type):
            name = name.decode('UTF-8', errors='escape')
        hashv = hashlib.sha1(s).hexdigest()
        hashv = hashv[:2] + os.path.sep + hashv[2:]
        ext = os.path.splitext(name)[1]
        dirname = os.path.dirname(name)
        filename = os.path.join(dirname, hashv + ext)
        return super(HashedStorageMixin, self)._save(filename, content)


class CachedHashValueFilesMixin(object):
    hash_map_filename = '.hash_map_filename'

    def __init__(self, *args, **kwargs):
        super(CachedHashValueFilesMixin, self).__init__(*args, **kwargs)
        self.hash_map = self.load_hash_map()

    def _load(self, filename):
        try:
            with self.open(filename) as fp:
                value = fp.read().decode('utf-8')
            return json.loads(value, object_pairs_hook=OrderedDict)
        except (IOError, ValueError):
            return OrderedDict()

    def load_hash_map(self):
        return self._load(self.hash_map_filename)

    def _save(self, name, content, *args, **kw):
        s = content.read()
        hashv = hashlib.sha1(s).hexdigest()
        if self.hash_map[name] == hashv:
            return name
        self.hash_map[name] = hashv
        return super(CachedHashValueFilesMixin, self)._save(name, content, *args, **kw)

    def _dump(self, filename, data):
        if self.exists(filename):
            self.delete(filename)
        contents = json.dumps(data).encode('utf-8')
        self._save(filename, ContentFile(contents))

    def post_process(self, *args, **kwargs):
        r = super(CachedHashValueFilesMixin, self).post_process(*args, **kwargs)
        self._dump(self.hash_map_filename, self.hash_map)
        self._dump(self.hashed_name_map_filename, self.hashed_name_map)
        return r


class CachedManifestFilesMixin(CachedHashValueFilesMixin, ManifestFilesMixin):
    hashed_name_map_filename = '.hashed_name_map_filename'

    def __init__(self, *args, **kwargs):
        super(CachedManifestFilesMixin, self).__init__(*args, **kwargs)
        self.hashed_name_map = self.load_hashed_name_map()

    def load_hashed_name_map(self):
        return self._load(self.hashed_name_map_filename)

    def _save(self, name, content, *args, **kw):
        s = content.read()
        hashv = hashlib.sha1(s).hexdigest()
        if self.hash_map[name] == hashv:
            return name
        self.hash_map[name] = hashv
        self.hashed_name_map.pop(name, None)
        return super(CachedManifestFilesMixin, self)._save(name, content, *args, **kw)

    def hashed_name(self, name, content=None, filename=None):
        if name in self.hashed_name_map:
            return self.hashed_name_map[name]
        return super(CachedManifestFilesMixin, self).hashed_name(name, content, filename)

    def post_process(self, *args, **kwargs):
        r = super(CachedManifestFilesMixin, self).post_process(*args, **kwargs)
        self._dump(self.hashed_name_map_filename, self.hashed_name_map)
        return r


class HashedFileSystemStorage(HashedStorageMixin, OverwriteStorageMixin, FileSystemStorage):
    IGNORE_OVERWRITE = True
