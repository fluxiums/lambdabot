import datetime
import os
import django
import discord

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lamdabotweb.settings")
django.setup()

NO_LIMIT_WHITELIST = [
    '257499042039332866',  # yackson
]

client = discord.Client()
meme_times = {}


@client.event
async def cmd_help(server, message):
    helpstr = "{0} available commands:".format(message.author.mention)
    for cmd_data in server.get_commands():
        helpstr += "\n**{0}{1}**".format(server.prefix, cmd_data.cmd)
        if cmd_data.help:
            helpstr += " - {0}".format(cmd_data.help)
    await client.send_message(message.channel, helpstr)


@client.event
async def cmd_meem(server, message):
    from memeviewer.models import Meem
    from memeviewer.preview import preview_meme
    from discordbot.models import DiscordMeem

    await client.send_typing(message.channel)

    if message.author.id not in NO_LIMIT_WHITELIST:
        meme_time_id = "{0}{1}".format(message.author.id, message.server.id)
        if meme_times.get(meme_time_id) is not None:
            if len(meme_times[meme_time_id]) == server.meme_limit_count:
                meme_delta = datetime.timedelta(minutes=server.meme_limit_time)
                meme_time = meme_times[meme_time_id][0]
                if datetime.datetime.now() - meme_delta > meme_time:
                    meme_times[meme_time_id].pop(0)
                else:
                    seconds_left = int(((meme_time + meme_delta) - datetime.datetime.now()).total_seconds()) + 1
                    if seconds_left >= 3 * 60:
                        timestr = "{0} more minutes".format(int(seconds_left / 60) + 1)
                    else:
                        timestr = "{0} more seconds".format(seconds_left)
                    await client.send_message(
                        message.channel,
                        "{3} you can only generate {0} memes every {1} minutes. Please wait {2}.".format(
                            server.meme_limit_count,
                            server.meme_limit_time,
                            timestr,
                            message.author.mention,
                        )
                    )
                    return
            meme_times[meme_time_id].append(datetime.datetime.now())
        else:
            meme_times[meme_time_id] = [datetime.datetime.now()]

    meme = Meem.generate(context=server.context)
    preview_meme(meme)

    discord_meme = DiscordMeem(meme=meme, server=message.server.id)
    discord_meme.save()

    await client.send_message(
        message.channel,
        content="{0} here's a meme:\n{1}".format(message.author.mention, meme.get_info_url())
    )

    print('meme generated:', message.author.name, meme)


CMD_FUN = {
    'help': cmd_help,
    'meem': cmd_meem,
}


@client.event
async def process_message(message):
    from memeviewer.models import Meem, MemeTemplate, sourceimg_count
    from discordbot.models import DiscordServer, DiscordCommand

    server_id = message.server.id
    server = DiscordServer.get_by_id(server_id)

    if server is None:
        return

    msg = message.content

    if client.user in message.mentions:
        await client.send_message(
            message.channel,
            "{0} LambdaBot is a bot which generates completely random Half-Life memes. It does this by picking a "
            "random meme template and combining it with one or more randomly picked source images related to "
            "Half-Life. Currently there are **{1:,}** available templates and **{2:,}** available source images, for a "
            "total of **{3:,}** possible combinations.\n"
            "\n"
            "Type **!help** to see a list of available commands.\n"
            "\n"
            "*Homepage: https://lambdabot.morchkovalski.com\n"
            "Created by morch kovalski (aka yackson): https://morchkovalski.com*".format(
                message.author.mention,
                MemeTemplate.count(server.context),
                sourceimg_count(server.context),
                Meem.possible_combinations(server.context)
            )
        )
        return
    elif not msg.startswith(server.prefix):
        return
    else:
        splitcmd = msg[len(server.prefix):].split(' ')

    cmd = DiscordCommand.get_cmd(splitcmd[0], server)

    if cmd is not None:
        if cmd.message is not None and len(cmd.message) > 0:
            await client.send_message(message.channel, cmd.message)

        cmd_fun = CMD_FUN.get(cmd.cmd)
        if cmd_fun is not None:
            await cmd_fun(server, message)


@client.event
async def on_message(message):
    await process_message(message)


@client.event
async def on_message_edit(_, message):
    await process_message(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='lambdabot.morchkovalski.com'))


from discord import Status, Server, Game, Channel
from memeviewer.models import AccessToken


# noinspection PyBroadException,PyArgumentList
def _sync_patched(self, data):
    if 'large' in data:
        self.large = data['large']

    for presence in data.get('presences', []):
        user_id = presence['user']['id']
        member = self.get_member(user_id)
        if member is not None:
            member.status = presence['status']
            try:
                member.status = Status(member.status)
            except:
                pass
            game = presence.get('game', {})
            try:
                member.game = Game(**game) if game else None
            except:
                member.game = None

    if 'channels' in data:
        channels = data['channels']
        for c in channels:
            channel = Channel(server=self, **c)
            self._add_channel(channel)


# noinspection PyUnresolvedReferences
Server._sync = _sync_patched
client.run(AccessToken.objects.get(name="discord").token)