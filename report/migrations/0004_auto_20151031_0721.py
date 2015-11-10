# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20151015_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='client',
            field=models.CharField(default=None, max_length=40, null=True, verbose_name='Zg\u0142aszaj\u0105cy', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Utworzone'),
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='report',
            name='resolved_at',
            field=models.DateTimeField(null=True, verbose_name='Rozpatrzone', blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='resolved_by',
            field=models.ForeignKey(verbose_name='Rozpatrzone przez', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]