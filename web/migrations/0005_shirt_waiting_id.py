# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150424_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='shirt',
            name='waiting_id',
            field=models.IntegerField(default=None),
        ),
    ]
