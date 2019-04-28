# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from django.db import models
from django.conf import settings

from django_busybody.rules import encrypt_field, save_history


class AllField(models.Model):
    # auto = models.AutoField()
    # big_auto = models.BigAutoField()
    big_integer = models.BigIntegerField()
    binary = models.BinaryField()
    boolean = models.BooleanField()
    char = models.CharField(max_length=128)
    # comma_separated_integer = models.CommaSeparatedIntegerField(max_length=128)
    date = models.DateField()
    date_time = models.DateTimeField()
    decimal = models.DecimalField(max_digits=20, decimal_places=2)
    duration = models.DurationField()
    email = models.EmailField()
    _file = models.FileField()
    file_path = models.FilePathField()
    _float = models.FloatField()
    # image = models.ImageField()
    integer = models.IntegerField()
    generic_ip_address = models.GenericIPAddressField()
    null_boolean = models.NullBooleanField()
    positive_integer = models.PositiveIntegerField()
    positive_small_integer = models.PositiveSmallIntegerField()
    slug = models.SlugField()
    small_integer = models.SmallIntegerField()
    text = models.TextField()
    time = models.TimeField()
    url = models.URLField()
    uuid = models.UUIDField()
    foreign_key = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)
    many_to_many = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+')
    one_to_one = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)


save_history(AllField)


class EncryptTest(models.Model):
    without_encrypt = models.CharField(max_length=256)
    with_encrypt = models.CharField(max_length=256)
    without_encrypt_with_log = models.CharField(max_length=256)
    with_encrypt_with_log = models.CharField(max_length=256)


save_history(EncryptTest, includes=[
    'without_encrypt_with_log',
    'with_encrypt_with_log'])

encrypt_field(EncryptTest, 'with_encrypt')
encrypt_field('tests.EncryptTest', 'with_encrypt_with_log')
