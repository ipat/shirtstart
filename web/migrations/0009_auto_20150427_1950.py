# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20150427_0106'),
    ]

    operations = [
        migrations.AddField(
            model_name='designer',
            name='bank_account_bank',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='bank_account_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='bank_account_number',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
