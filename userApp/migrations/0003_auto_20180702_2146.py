# Generated by Django 2.0.2 on 2018-07-02 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0002_auto_20180702_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofileinfo',
            old_name='users',
            new_name='user',
        ),
    ]
