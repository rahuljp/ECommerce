# Generated by Django 2.0.2 on 2018-07-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoryApp', '0008_auto_20180704_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=120)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.CharField(default='Samsung', max_length=120),
        ),
    ]
