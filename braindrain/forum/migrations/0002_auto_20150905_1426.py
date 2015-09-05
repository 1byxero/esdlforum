# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='answer',
            fields=[
                ('aid', models.IntegerField(serialize=False, primary_key=True)),
                ('answercontent', models.CharField(max_length=2000)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='questionsanswered',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='questionsasked',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to='forum.user'),
        ),
    ]
