# ---       IMPORTS          ---#


import discord
import unicodedata
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib.request import Request, urlopen

# ---       GLOBAL VARIABLES          ---#


# bs4
site = "https://coinmarketcap.com/all/views/all/"
hdr = {'User-Agent': 'Mozilla/84.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, 'html.parser')

site2 = "https://coinranking.com/"
hdr2 = {'User-Agent': 'Mozilla/84.0'}
req2 = Request(site2, headers=hdr2)
page2 = urlopen(req2)
soup2 = BeautifulSoup(page2, 'html.parser')

# dicts
coin_icons = {}
coin_names = {}
coin_prices = {}
coin_market_cap = {}

# links
bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'


# ---       FUNCTIONS        --- #

def icons():
    counter = 1
    for png in soup2.find_all('span', class_='profile__logo-background'):
        png = png.img.get('src')
        png = png.strip('?size=30x3048x48')
        png = png.replace('.svg', '.png')
        coin_icons[counter] = png
        counter += 1


def names():
    counter = 1
    for name in soup.find_all('div', class_='sc-1kxikfi-0 fjclfm cmc-table__column-name'):
        name = name.text
        coin_names[counter] = name
        counter += 1


def prices():
    counter = 1
    for price in soup.find_all('div', class_='price___3rj7O'):
        price = price.text
        price = price.strip()
        coin_prices[counter] = price
        counter += 1

# ---     CUSTOM CHECKS     --- #


def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       ---#


class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(bot_channel_check)
    async def crypto(self, ctx, coin_number):
        names()
        icons()
        prices()
        emoji_list = ['◀', '▶']

        embed = discord.Embed(
            title=str(coin_prices.get(int(coin_number))),
            description=' ',
            colour=discord.Colour.blurple()
        )
        embed.set_footer(text=site)
        if 0 < int(coin_number) <= 50:
            embed.set_author(
                name=f'{coin_number}. {str(coin_names.get(int(coin_number)))}',
                icon_url=coin_icons.get(int(coin_number))
            )
        else:
            embed = discord.Embed(
                title='Invalid Number',
                description=' ',
                colour=discord.Colour.red()
            )

        message_embed = await ctx.send(embed=embed)
        for emoji in emoji_list:
            await message_embed.add_reaction(emoji)

    @crypto.error
    async def crypto_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error: Specify crypto #',
                description=' ',
                colour=discord.Colour.red()
            )
            embed.set_footer(text='ex => ;crypto 1')

            await ctx.send(embed=embed, delete_after=5)

    @commands.command()
    @commands.check(bot_channel_check)
    async def cryptolist(self, ctx, page):
        names()
        prices()
        emoji_list = ['◀', '▶']

        embed = discord.Embed(
            title=' ',
            description=' ',
            colour=discord.Colour.blurple()
        )

        embed.set_author(name=f'Top {10 * int(page)} Crypto Coins',
                         icon_url=bot_avatar_link)
        embed.set_footer(text=site)
        if page == '1':
            counter = 1
            while counter < 11:
                embed.add_field(name=f'{counter}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '2':
            counter = 11
            while counter < 21:
                embed.add_field(name=f'{counter}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '3':
            counter = 21
            while counter < 31:
                embed.add_field(name=f'{counter}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '4':
            counter = 31
            while counter < 41:
                embed.add_field(name=f'{counter}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '5':
            counter = 41
            while counter < 51:
                embed.add_field(name=f'{counter}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1

        message_embed = await ctx.send(embed=embed)
        for emoji in emoji_list:
            await message_embed.add_reaction(emoji)

    @cryptolist.error
    async def cryptolist_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error: Specify cryptolist #',
                description=' ',
                colour=discord.Colour.red()
            )
            embed.set_footer(text='ex => ;cryptolist 1')

            await ctx.send(embed=embed, delete_after=5)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Market(bot))
