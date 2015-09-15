# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_user_isteacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='onetoonequestions',
            fields=[
                ('qid', models.IntegerField(serialize=False, primary_key=True)),
                ('questiontitle', models.CharField(max_length=200)),
                ('questioncontent', models.TextField()),
                ('answered', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='questionsanswered',
        ),
        migrations.RemoveField(
            model_name='user',
            name='questionsasked',
        ),
        migrations.AddField(
            model_name='onetoonequestions',
            name='askedby',
            field=models.ForeignKey(related_name='askedby', to='forum.user'),
        ),
        migrations.AddField(
            model_name='onetoonequestions',
            name='askedto',
            field=models.ForeignKey(related_name='askedto', to='forum.user'),
        ),
    ]
