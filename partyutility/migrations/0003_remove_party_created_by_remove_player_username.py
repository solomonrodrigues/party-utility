# Generated by Django 4.1.3 on 2025-02-25 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partyutility', '0002_remove_player_user_player_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='player',
            name='username',
        ),
    ]
