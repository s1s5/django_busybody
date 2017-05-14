# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import django
from django.test import TestCase
from django.conf import settings
# from django.core.urlresolvers import reverse

import django_busybody.models as bb_models


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
