# Generated by Django 2.0.3 on 2020-02-28 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20200229_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='EOBTrevision',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='typeChange',
            field=models.CharField(max_length=10, null=True),
        ),
    ]