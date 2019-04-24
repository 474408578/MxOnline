# Generated by Django 2.1 on 2019-04-15 02:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190414_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.png', upload_to='image/%Y/%m'),
        ),
    ]