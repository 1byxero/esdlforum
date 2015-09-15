# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20150911_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isteacher',
            field=models.BooleanField(default=False),
        ),
    ]
