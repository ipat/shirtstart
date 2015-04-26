# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20150426_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ship_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_tracking_no',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
