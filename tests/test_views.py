# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from django.test import TestCase
# from django.core.urlresolvers import reverse

import django_busybody.models as bb_models


class TestDjango_view(TestCase):

    def test_admin(self):
        m = bb_models.History
        info = (m._meta.app_label, m._meta.model_name)
        self.client.get('admin:{}_{}_add'.format(*info))
