import discord
import re
import asyncio
import lamdabotweb.settings as config
from django.core.management import BaseCommand
from discord.ext import commands
from django.core.exceptions import ObjectDoesNotExist
from discordbot.models import DiscordServer, DiscordContext
from util import log


class Command(BaseCommand):
    help = 'Starts the discord bot'
    bot = None

    def handle(self, *args, **options):
        bot = commands.Bot(command_prefix=config.DISCORD_CMD_PREFIX, description='I make memes.')

        @bot.event
        async def on_guild_join(server: discord.Guild):
            DiscordServer.get(server)

        @bot.event
        async def on_member_update(_, member: discord.Member):
            try:
                server_data = DiscordServer.get(member.guild)
                user_data = server_data.get_member(member)
                user_data.update(member)
            except ObjectDoesNotExist:
                pass

        @bot.event
        async def on_guild_update(_, server: discord.Guild):
            try:
                server_data = DiscordServer.get(server)
                server_data.update(server.name)
            except ObjectDoesNotExist:
                pass

        @bot.event
        async def on_ready():
            log('Logged in as', bot.user.name, bot.user.id)
            await bot.change_presence(activity=discord.Game(name=config.DISCORD_STATUS))

        @bot.event
        async def on_message(msg: discord.Message):
            if re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                         msg.content) is not None:
                await asyncio.sleep(3)

            ctx = await bot.get_context(msg, cls=DiscordContext)
            if ctx.valid:
                await bot.invoke(ctx)

        for cog_name in config.DISCORD_COGS:
            bot.load_extension('discordbot.cogs.' + cog_name)

        bot.run(config.DISCORD_TOKEN)