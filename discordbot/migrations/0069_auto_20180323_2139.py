# Generated by Django 2.0 on 2018-03-23 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0068_remove_discordserveruser_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discordserver',
            name='context',
            field=models.ForeignKey(default='default', on_delete=django.db.models.deletion.SET_DEFAULT, to='memeviewer.MemeContext', verbose_name='Context'),
        ),
    ]
