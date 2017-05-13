# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 13:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('big_integer', models.BigIntegerField()),
                ('binary', models.BinaryField()),
                ('boolean', models.BooleanField()),
                ('char', models.CharField(max_length=128)),
                ('comma_separated_integer', models.CommaSeparatedIntegerField(max_length=128)),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('decimal', models.DecimalField(decimal_places=2, max_digits=20)),
                ('duration', models.DurationField()),
                ('email', models.EmailField(max_length=254)),
                ('_file', models.FileField(upload_to='')),
                ('file_path', models.FilePathField()),
                ('_float', models.FloatField()),
                ('integer', models.IntegerField()),
                ('generic_ip_address', models.GenericIPAddressField()),
                ('null_boolean', models.NullBooleanField()),
                ('positive_integer', models.PositiveIntegerField()),
                ('positive_small_integer', models.PositiveSmallIntegerField()),
                ('slug', models.SlugField()),
                ('small_integer', models.SmallIntegerField()),
                ('text', models.TextField()),
                ('time', models.TimeField()),
                ('url', models.URLField()),
                ('uuid', models.UUIDField()),
                ('foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('many_to_many', models.ManyToManyField(related_name='_allfield_many_to_many_+', to=settings.AUTH_USER_MODEL)),
                ('one_to_one', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
