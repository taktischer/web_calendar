# Generated by Django 4.2.4 on 2023-11-29 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='title',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]