# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import codecs
import zipfile

import sys
if sys.version_info[0] < 3:
    from backports import csv
else:
    import csv


class CsvDataMixin(object):
    encoding = 'UTF-8'
    delimiter = ','

    def get_encoding(self):
        return self.encoding

    def get_delimiter(self):
        return self.delimiter

    def write_data(self, buf):
        csv_writer = csv.writer(
            codecs.getwriter(self.get_encoding())(buf, errors='replace'),
            delimiter=self.get_delimiter())
        for row in self.get_rows():
            csv_writer.writerow(row)


class ZipDataMixin(object):
    def write_data(self, buf):
        zf = zipfile.ZipFile(buf, 'w')
        for path, content in self.get_files():
            zf.writestr(path, content)
        zf.close()
