# Generated by Django 2.0.3 on 2020-03-04 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_printingsetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printingsetting',
            name='minutesDiff',
            field=models.FloatField(max_length=5, null=True),
        ),
    ]
