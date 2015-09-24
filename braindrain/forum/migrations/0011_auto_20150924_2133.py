# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20150924_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tag1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tag2',
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.ForeignKey(blank=True, to='forum.tags', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='askedto',
            field=models.ForeignKey(related_name='askedto', blank=True, to='forum.user', null=True),
        ),
    ]
