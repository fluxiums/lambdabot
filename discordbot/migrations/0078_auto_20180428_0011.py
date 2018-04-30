# Generated by Django 2.0 on 2018-04-27 22:11

from django.db import migrations


def do_stuff(apps, schema_editor):
    MemeImagePool = apps.get_model('memeviewer', 'MemeImagePool')
    DiscordMeem = apps.get_model('discordbot', 'DiscordMeem')
    DiscordChannel = apps.get_model('discordbot', 'DiscordChannel')
    hldpool = MemeImagePool.objects.get(name='hldiscord')
    halflifepool = MemeImagePool.objects.get(name='halflife')
    for i in DiscordMeem.objects.all():
        ch = DiscordChannel.objects.get_or_create(channel_id=i.channel_id, defaults={'server': i.discord_server})[0]
        ch.submission_pool = halflifepool
        ch.image_pools.add(halflifepool)
        if i.discord_server and i.discord_server.server_id in ['154305477323390976', '348938395999010827', '368440132166221835']:
            ch.image_pools.add(hldpool)
        ch.save()
        i.discord_channel = ch
        i.save()
    DiscordChannel.objects.filter(channel_id='0').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0077_auto_20180428_0004'),
    ]

    operations = [
        migrations.RunPython(do_stuff)
    ]