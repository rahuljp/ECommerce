# Generated by Django 2.0.2 on 2018-07-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0003_auto_20180702_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
    ]