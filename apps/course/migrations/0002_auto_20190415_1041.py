# Generated by Django 2.1 on 2019-04-15 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='download',
            field=models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件'),
        ),
    ]
