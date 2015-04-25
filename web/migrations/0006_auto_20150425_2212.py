# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_shirt_waiting_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waiting',
            name='shirt_id',
        ),
        migrations.AlterField(
            model_name='shirt',
            name='waiting_id',
            field=models.ForeignKey(to='web.Waiting'),
        ),
    ]
