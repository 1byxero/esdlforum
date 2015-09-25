# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_auto_20150924_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='tempusers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200)),
                ('hashlink', models.CharField(max_length=200)),
            ],
        ),
    ]
