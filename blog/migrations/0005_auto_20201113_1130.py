# Generated by Django 3.1 on 2020-11-13 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_user_profile_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
