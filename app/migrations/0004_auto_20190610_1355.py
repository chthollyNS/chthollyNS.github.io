# Generated by Django 2.0.1 on 2019-06-10 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20190610_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='read',
            field=models.TextField(default=''),
        ),
    ]