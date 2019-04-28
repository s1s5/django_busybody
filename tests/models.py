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
    big_integer = models.BigIntegerField(blank=True, null=True)
    binary = models.BinaryField(blank=True, null=True)
    boolean = models.BooleanField(default=False)
    char = models.CharField(max_length=128, blank=True, null=True)
    # comma_separated_integer = models.CommaSeparatedIntegerField(max_length=128)
    date = models.DateField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    decimal = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    _file = models.FileField(blank=True, null=True)
    file_path = models.FilePathField(blank=True, null=True)
    _float = models.FloatField(blank=True, null=True)
    # image = models.ImageField()
    integer = models.IntegerField(blank=True, null=True)
    generic_ip_address = models.GenericIPAddressField(blank=True, null=True)
    null_boolean = models.NullBooleanField(blank=True, null=True)
    positive_integer = models.PositiveIntegerField(blank=True, null=True)
    positive_small_integer = models.PositiveSmallIntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    small_integer = models.SmallIntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    uuid = models.UUIDField(blank=True, null=True)
    foreign_key = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                    related_name='+', on_delete=models.CASCADE)
    many_to_many = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='+')
    one_to_one = models.OneToOneField(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+', on_delete=models.CASCADE)


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
