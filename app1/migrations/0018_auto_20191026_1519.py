# Generated by Django 2.2.4 on 2019-10-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_flight_dateto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='DayofWeek',
            field=models.CharField(choices=[('1', 'sun'), ('2', 'mon'), ('3', 'tue'), ('4', 'wed'), ('5', 'thr'), ('6', 'fri'), ('7', 'sat')], default=None, max_length=20, null=True),
        ),
    ]