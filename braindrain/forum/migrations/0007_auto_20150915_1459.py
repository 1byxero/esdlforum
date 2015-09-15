# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20150915_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onetoonequestions',
            name='askedby',
        ),
        migrations.RemoveField(
            model_name='onetoonequestions',
            name='askedto',
        ),
        migrations.AddField(
            model_name='question',
            name='askedto',
            field=models.ForeignKey(related_name='askedto', to='forum.user', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='isonetoone',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='askedby',
            field=models.ForeignKey(related_name='askedby', to='forum.user'),
        ),
        migrations.DeleteModel(
            name='onetoonequestions',
        ),
    ]
