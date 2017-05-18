# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import io
import zipfile

import django
from django.test import TestCase
from django.conf import settings
from django import forms
from django.views import generic
from django.test.client import RequestFactory
# from django.core.urlresolvers import reverse

import django_busybody.models as bb_models
import django_busybody.views as bb_views


class TestDjango_view(TestCase):

    def test_admin(self):
        m = bb_models.History
        info = (m._meta.app_label, m._meta.model_name)
        self.client.get('admin:{}_{}_add'.format(*info))

    def test_without_midleware(self):
        attr_name = 'MIDDLEWARE_CLASSES'
        if django.VERSION >= (1, 10):
            attr_name = 'MIDDLEWARE'
        org_value = getattr(settings, attr_name)
        copied = list(org_value)
        copied.remove('django_busybody.middlewares.GlobalRequestMiddleware')
        setattr(settings, attr_name, copied)

        m = bb_models.History
        info = (m._meta.app_label, m._meta.model_name)
        self.client.get('admin:{}_{}_add'.format(*info))

        setattr(settings, attr_name, org_value)


class TestForm(forms.Form):
    t = forms.CharField()


class TestFormView(bb_views.SearchFormMixin, generic.TemplateView):
    form_class = TestForm
    template_name = 'test_form.html'


class DownloadMixin(object):
    def get(self, *args, **kwargs):
        return self.download(**kwargs)


class TestDownloadView(DownloadMixin, bb_views.DownloadMixin, generic.TemplateView):
    template_name = 'test_form.html'

    def write_data(self, buf, *args, **kwargs):
        buf.write('日本語'.encode('UTF-8'))


class TestDownloadCsvView(DownloadMixin, bb_views.DownloadCsvMixin, generic.View):
    def get_rows(self):
        yield ['value', '日本語']


class TestDownloadZipView(DownloadMixin, bb_views.DownloadZipMixin, generic.View):
    def get_files(self):
        yield 'path', b'contents'


class TestDjango_search_form_mixin(TestCase):

    def test_view(self):
        request = RequestFactory().get('/some_url/')
        response = TestFormView.as_view()(request).render()
        # print(response)
        self.assertContains(response, 'id="id_t"')
        self.assertContains(response, 'name="t"')
        # ちゃんとformをGETしたら値が入って戻ってくるかチェック

    def test_download(self):
        request = RequestFactory().get('/some_url/')
        response = TestDownloadView.as_view()(request)
        self.assertEqual(response.content.decode('UTF-8'), '日本語')

    def test_download_csv(self):
        request = RequestFactory().get('/some_url/')
        response = TestDownloadCsvView.as_view()(request)
        self.assertEqual(response.content.decode('UTF-8').strip(), 'value,日本語')

    def test_download_zip(self):
        request = RequestFactory().get('/some_url/')
        response = TestDownloadZipView.as_view()(request)
        buf = io.BytesIO(response.content)
        with zipfile.ZipFile(buf, 'r') as zf:
            for path in zf.namelist():
                self.assertEqual(path, 'path')
                self.assertEqual(zf.read(path), b'contents')
