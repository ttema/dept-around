# Generated by Django 3.0.4 on 2020-05-31 11:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
