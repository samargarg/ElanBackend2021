# Generated by Django 3.1.5 on 2021-01-14 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbassadorDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('picture', models.URLField(max_length=500)),
                ('instagram', models.CharField(blank=True, max_length=200, null=True)),
                ('facebook', models.CharField(blank=True, max_length=200, null=True)),
                ('institute', models.CharField(blank=True, max_length=200, null=True)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ManagerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('completed', models.BooleanField()),
                ('max_points', models.IntegerField()),
                ('points_awarded', models.IntegerField(default=0)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_assigned_to_me', to=settings.AUTH_USER_MODEL)),
                ('assigner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_assigned_by_me', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=500)),
                ('by_manager', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_reply', models.BooleanField(default=False)),
                ('replied_to', models.CharField(blank=True, max_length=500, null=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
