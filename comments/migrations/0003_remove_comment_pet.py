# Generated by Django 3.2.19 on 2023-05-20 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20230518_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='pet',
        ),
    ]
