# Generated by Django 3.0.4 on 2020-06-02 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20200531_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='x',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='y',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='payment',
            name='x',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='payment',
            name='y',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
