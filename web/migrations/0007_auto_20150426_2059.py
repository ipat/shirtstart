# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20150425_2212'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='join',
            unique_together=set([('user_id', 'shirt_id', 'shirt_size', 'time')]),
        ),
    ]
