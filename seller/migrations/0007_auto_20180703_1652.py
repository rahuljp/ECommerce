# Generated by Django 2.0.2 on 2018-07-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0006_auto_20180703_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='medium',
            name='company',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='medium',
            name='model',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]