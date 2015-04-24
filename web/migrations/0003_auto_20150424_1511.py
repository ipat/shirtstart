# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150424_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_designer',
            field=models.BooleanField(default=False),
        ),
    ]
