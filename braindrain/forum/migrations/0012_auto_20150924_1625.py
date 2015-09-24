# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20150924_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='tagid',
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=30, serialize=False, primary_key=True),
        ),
    ]
