# Generated by Django 2.2.16 on 2022-07-17 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20220717_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='author',
        ),
    ]