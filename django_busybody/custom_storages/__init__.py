# coding: utf-8
from .chain import ChainStorage  # NOQA
try:
    from .s3 import StaticS3Storage, ManifestFilesStaticS3Storage,MediaS3Storage  # NOQA
except ImportError:
    raise
