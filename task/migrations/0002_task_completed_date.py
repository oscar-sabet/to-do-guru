# Generated by Django 4.2.7 on 2025-03-07 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
