# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models
from django.conf import settings


class AllField(models.Model):
    # auto = models.AutoField()
    # big_auto = models.BigAutoField()
    big_integer = models.BigIntegerField()
    binary = models.BinaryField()
    boolean = models.BooleanField()
    char = models.CharField(max_length=128)
    comma_separated_integer = models.CommaSeparatedIntegerField(max_length=128)
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
    foreign_key = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    many_to_many = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+')
    one_to_one = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='+')
