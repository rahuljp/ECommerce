# Generated by Django 2.0.2 on 2018-07-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoryApp', '0007_auto_20180703_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(choices=[('Laptop', 'Laptop'), ('Smartphone', 'Smartphone'), ('TVs', 'TVs')], default='Laptop', max_length=120),
        ),
    ]
