# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20150921_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tag1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tag2',
        ),
        migrations.AddField(
            model_name='question',
            name='tag1',
            field=models.ForeignKey(related_name='tag1', to='forum.tags', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='tag2',
            field=models.ForeignKey(related_name='tag2', to='forum.tags', null=True),
        ),
    ]
