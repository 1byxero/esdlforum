# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150905_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('qid', models.IntegerField(serialize=False, primary_key=True)),
                ('questiontitle', models.CharField(max_length=200)),
                ('questioncontent', models.TextField()),
                ('answered', models.BooleanField(default=False)),
                ('askedby', models.ForeignKey(to='forum.user')),
            ],
        ),
        migrations.AlterField(
            model_name='answer',
            name='answercontent',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='forum.question', null=True),
        ),
    ]
