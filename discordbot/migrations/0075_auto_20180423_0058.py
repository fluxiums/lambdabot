# Generated by Django 2.0 on 2018-04-22 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0073_auto_20180423_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordmeem',
            name='discord_server',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discordbot.DiscordServer'),
        ),
        migrations.AddField(
            model_name='discordsourceimgsubmission',
            name='discord_server',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='discordbot.DiscordServer'),
        ),
    ]
