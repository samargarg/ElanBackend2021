# Generated by Django 3.1.5 on 2021-01-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caportal', '0003_auto_20210111_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambassadordetail',
            name='picture',
            field=models.URLField(max_length=500),
        ),
    ]
