# Generated by Django 3.1 on 2020-11-12 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_completed',
        ),
    ]
