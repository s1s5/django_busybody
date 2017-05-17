# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import io

from django.test import TestCase
from django.utils.encoding import force_text

import django_busybody.views as bb_datas


class TestDjango_datas(TestCase):
    line0 = ['header', 'ヘッダ']
    line1 = ['value', '値']

    def get_rows(self):
        yield self.line0
        yield self.line1

    def test_csv_0(self):
        csv_data = bb_datas.CsvDataMixin()
        csv_data.get_rows = self.get_rows
        buf = io.BytesIO()
        csv_data.write_data(buf)
        buf.seek(0)
        rows = csv_data.read_data(buf)
        self.assertEqual(next(rows), self.line0)
        self.assertEqual(next(rows), self.line1)

    def test_csv_1(self):
        csv_data = bb_datas.CsvDataMixin()
        buf = io.BytesIO()
        csv_data.write_data(buf, [self.line0, self.line1])
        buf.seek(0)
        rows = csv_data.read_data(buf)
        self.assertEqual(next(rows), self.line0)
        self.assertEqual(next(rows), self.line1)

    def test_csv_2(self):
        csv_data = bb_datas.CsvDataMixin()
        buf = io.BytesIO()
        csv_data.write_data(buf, [])
        buf.seek(0)
        rows = csv_data.read_data(buf)
        self.assertEqual(len(list(rows)), 0)

    contents_map = {
        'key0': 'contents0',
        'キー1': '日本語',
    }

    def get_files(self):
        for path, contents in self.contents_map.items():
            yield path, contents

    def test_zip0(self):
        zip_data = bb_datas.ZipDataMixin()
        buf = io.BytesIO()
        zip_data.get_files = self.get_files
        zip_data.write_data(buf)
        buf.seek(0)
        for path, content in zip_data.read_data(buf):
            self.assertEqual(force_text(content), self.contents_map[path])

    def test_zip1(self):
        zip_data = bb_datas.ZipDataMixin()
        buf = io.BytesIO()
        zip_data.write_data(buf, self.contents_map.items())
        buf.seek(0)
        for path, content in zip_data.read_data(buf):
            self.assertEqual(force_text(content), self.contents_map[path])
