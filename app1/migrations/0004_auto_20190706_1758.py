# Generated by Django 2.1.5 on 2019-07-06 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20190706_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=20, null=True),
        ),
    ]
