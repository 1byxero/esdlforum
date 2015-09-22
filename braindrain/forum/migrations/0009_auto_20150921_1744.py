# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_remove_user_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='tags',
            fields=[
                ('tagid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='tag1',
            field=models.ForeignKey(related_name='tag1', to='forum.tags', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='tag2',
            field=models.ForeignKey(related_name='tag2', to='forum.tags', null=True),
        ),
    ]
