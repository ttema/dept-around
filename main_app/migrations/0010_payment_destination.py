# Generated by Django 3.0.4 on 2020-06-06 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20200606_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='destination',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
