# Generated by Django 2.0 on 2018-04-22 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0074_auto_20180423_0033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discordmeem',
            name='server_user',
        ),
        migrations.RemoveField(
            model_name='discordsourceimgsubmission',
            name='server_user',
        ),
        migrations.AlterField(
            model_name='discordmeem',
            name='channel_id',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
    ]
