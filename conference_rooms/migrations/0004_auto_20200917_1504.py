# Generated by Django 3.1.1 on 2020-09-17 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference_rooms', '0003_auto_20200916_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(),
        ),
    ]
