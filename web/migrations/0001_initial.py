# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Credit_card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=30)),
                ('expiry_year', models.CharField(max_length=5)),
                ('expiry_month', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bank_account_name', models.CharField(max_length=100)),
                ('bank_account_number', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt_size', models.CharField(max_length=5)),
                ('amount', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('address_house_no', models.CharField(max_length=10)),
                ('address_building', models.CharField(max_length=50)),
                ('address_road', models.CharField(max_length=50)),
                ('address_subdistrict', models.CharField(max_length=50)),
                ('address_district', models.CharField(max_length=50)),
                ('address_province', models.CharField(max_length=50)),
                ('address_country', models.CharField(max_length=20)),
                ('address_postcode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('ship_date', models.DateField()),
                ('ship_tracking_no', models.CharField(max_length=20)),
                ('status', models.IntegerField()),
                ('address_house_no', models.CharField(max_length=10)),
                ('address_building', models.CharField(max_length=50)),
                ('address_road', models.CharField(max_length=50)),
                ('address_subdistrict', models.CharField(max_length=50)),
                ('address_district', models.CharField(max_length=50)),
                ('address_province', models.CharField(max_length=50)),
                ('address_country', models.CharField(max_length=20)),
                ('address_postcode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt_size', models.CharField(max_length=5)),
                ('amount', models.IntegerField()),
                ('price_each', models.DecimalField(decimal_places=2, max_digits=5)),
                ('order_id', models.ForeignKey(to='web.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Shirt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('file_url', models.FileField(upload_to=b'')),
                ('shirt_color', models.IntegerField()),
                ('is_on_shelf', models.BooleanField()),
                ('color_num', models.IntegerField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Shirt_in_cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt_size', models.CharField(max_length=5)),
                ('amount', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('shirt_id', models.ForeignKey(to='web.Shirt')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.DateTimeField()),
                ('to_account_bank', models.CharField(max_length=30)),
                ('to_account_number', models.CharField(max_length=30)),
                ('to_account_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_first', models.CharField(max_length=50)),
                ('name_last', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], max_length=1)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('birthdate', models.DateField()),
                ('is_designer', models.BooleanField()),
                ('address_house_no', models.CharField(max_length=10)),
                ('address_building', models.CharField(max_length=50)),
                ('address_road', models.CharField(max_length=50)),
                ('address_subdistrict', models.CharField(max_length=50)),
                ('address_district', models.CharField(max_length=50)),
                ('address_province', models.CharField(max_length=50)),
                ('address_country', models.CharField(max_length=20)),
                ('address_postcode', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Waiting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('require_amount', models.IntegerField()),
                ('require_date', models.DateField()),
                ('shirt_id', models.OneToOneField(to='web.Shirt')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='user_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AddField(
            model_name='shirt_in_cart',
            name='user_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='owner_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AddField(
            model_name='order_list',
            name='shirt_id',
            field=models.ForeignKey(to='web.Shirt'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AddField(
            model_name='like',
            name='shirt_id',
            field=models.ForeignKey(to='web.Shirt'),
        ),
        migrations.AddField(
            model_name='like',
            name='user_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AddField(
            model_name='join',
            name='shirt_id',
            field=models.ForeignKey(to='web.Shirt'),
        ),
        migrations.AddField(
            model_name='join',
            name='user_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AddField(
            model_name='designer',
            name='user_id',
            field=models.OneToOneField(to='web.User'),
        ),
        migrations.AddField(
            model_name='credit_card',
            name='user_id',
            field=models.OneToOneField(to='web.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='shirt_id',
            field=models.ForeignKey(to='web.Shirt'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(to='web.User'),
        ),
        migrations.AlterUniqueTogether(
            name='shirt_in_cart',
            unique_together=set([('user_id', 'shirt_id', 'shirt_size')]),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user_id', 'shirt_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='join',
            unique_together=set([('user_id', 'shirt_id', 'shirt_size')]),
        ),
    ]
