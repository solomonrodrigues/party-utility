# Generated by Django 4.1.3 on 2025-02-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partyutility', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.AddField(
            model_name='player',
            name='username',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
