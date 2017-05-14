# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

from django.test import TestCase
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings


class TestDjango_password(TestCase):

    def setUp(self):
        self.org_validators = settings.AUTH_PASSWORD_VALIDATORS
        settings.AUTH_PASSWORD_VALIDATORS = self.org_validators + [
            {
                'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
                'OPTIONS': {
                    'min_length': 8,
                }
            },
            {
                'NAME': 'django_busybody.validators.AlNumPasswordValidator',
            },
            {
                'NAME': 'django_busybody.validators.SimplePasswordValidator',
            },
            {
                'NAME': 'django_busybody.validators.CheckIdPasswordValdiator',
            },
        ]
        for i in settings.AUTH_PASSWORD_VALIDATORS:
            if i['NAME'] == 'django.contrib.auth.password_validation.MinimumLengthValidator':
                i['OPTIONS']['min_length'] = 8

    def tearDown(self):
        settings.AUTH_PASSWORD_VALIDATORS = self.org_validators

    def valid_password(self, password):
        validate_password(password)

    def invalid_password(self, password, user=None):
        try:
            validate_password(password, user)
        except ValidationError:
            pass
        else:
            raise Exception('{} accepted'.format(password))

    def test_acceptable(self):
        pass_list = [
            'ab111111',
            'XY111111',
            'aX111111',
            'a1111112',
            'X1111112',
            '1111112X',
            '6u9AHB2W',
            '55QScBd2',
            'r730nWGt',
            'fsDX2SaH',
            '1VShvcEO',
        ]
        [self.valid_password(x) for x in pass_list]
        [self.valid_password(x[::-1]) for x in pass_list]

    def test_7(self):
        pass_list = [
            'x',
            'x1',
            'xy1',
            'xy12z',
            'xy12zc',
            'xy12zcy']
        [self.invalid_password(x) for x in pass_list]

    def test_alphabet_only(self):
        pass_list = [
            'nfswaosg',
            'xezgxnet',
            'UHGHJVQL',
            'NCCXXSGJ',
            'SGWBISaD',
            'RrNefaQm',
            'JPoeBiDC', ]
        [self.invalid_password(x) for x in pass_list]

    def test_number_only(self):
        pass_list = [
            '92849946',
            '00408727',
            '11822307',
            '12789825',
            '86229927',
        ]
        [self.invalid_password(x) for x in pass_list]

    def test_2char(self):
        pass_list = [
            'a9a9a9a9',
            'b2b2b2b2',
        ]
        [self.invalid_password(x) for x in pass_list]

    def test_id(self):
        u0 = get_user_model().objects.create(username="XY12345678")
        u1 = get_user_model().objects.create(username="XY23456789")
        pass_list = [
            ('XY12345678', u0),
            ('XY23456789', u1),
        ]
        [self.invalid_password(x[0], x[1]) for x in pass_list]
