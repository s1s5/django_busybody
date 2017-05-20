# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from django.test import TestCase
from django.conf.urls import url
from django.views.generic import TemplateView

from django_busybody import decorators


class RequiredTest(TestCase):
    def _wrapper(self, func):
        func.wrapped = True
        return func

    def test_decorate(self):
        patterns = decorators.required(
            self._wrapper,
            [
                url(r'', TemplateView.as_view(template_name="base.html")),
            ]
        )
        for p in patterns:
            self.assertTrue(getattr(p.resolve('').func, 'wrapped'))
