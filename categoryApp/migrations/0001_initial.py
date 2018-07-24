# Generated by Django 2.0.2 on 2018-05-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Laptops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('launch_date', models.DateField()),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmartPhones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('launch_date', models.DateField()),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]