# Generated by Django 3.1.5 on 2021-01-11 20:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('caportal', '0004_auto_20210111_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('completed', models.BooleanField()),
                ('points', models.IntegerField()),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_assigned_to_me', to=settings.AUTH_USER_MODEL)),
                ('assigner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_assigned_by_me', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]