import json
import requests
from discord.ext import commands
from discord.ext.commands import Bot, Context, CommandError, Cog
from util import headers


class GarfieldCog(Cog):
    def __init__(self, bot: Bot):
        self.__cog_name__ = "Garfield"
        self.bot = bot

    @commands.command(name='gfwiki')
    async def cmd_wiki(self, ctx: Context, *, query=None):
        """
        search the garfield wiki
        if no argument is given shows a random article
        """
        wiki_url = 'http://garfield.wikia.com'
        article_url = None

        async with ctx.typing():
            if not query:
                response = requests.get(
                    '{0}/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json'.format(wiki_url),
                    headers=headers,
                )
                article_data = json.loads(response.text)
                article_id = article_data['query']['random'][0]['id']

                response = requests.get(
                    '{0}/api/v1/Articles/Details?ids={1}'.format(wiki_url, article_id),
                    headers=headers,
                )
                article_data = json.loads(response.text)
                article_url = "{0}{1}".format(
                    wiki_url,
                    article_data['items'][str(article_id)]['url']
                )

            else:
                response = requests.get(
                    '{0}/api/v1/Search/List?query={1}&limit=1'.format(wiki_url, query),
                    headers=headers,
                )
                article_data = json.loads(response.text)
                if article_data.get('exception') is None:
                    article_url = article_data['items'][0]['url']

        if article_url is None:
            raise CommandError("article not found :cry:")
        else:
            await ctx.send("{} {}".format(ctx.author.mention, article_url))


def setup(bot: Bot):
    bot.add_cog(GarfieldCog(bot))
