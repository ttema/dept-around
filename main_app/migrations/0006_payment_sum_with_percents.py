# Generated by Django 3.0.4 on 2020-06-02 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200602_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='sum_with_percents',
            field=models.IntegerField(default=0),
        ),
    ]
