# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 13:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_busybody', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='changes_json',
            new_name='changes',
        ),
        migrations.AddField(
            model_name='history',
            name='uri',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='who',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
