# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prebeca', '0024_auto_20150523_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='imagen',
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(default=1, to='prebeca.User'),
            preserve_default=False,
        ),
    ]
