# ---       IMPORTS          ---#


import discord
import unicodedata
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib.request import Request, urlopen

# ---       GLOBAL VARIABLES          ---#


# bs4
site = "https://coinlib.io/coins"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, 'html.parser')

# dicts
coin_links = {}
coin_icons = {}
coin_names = {}
coin_percent = {}
coin_prices = {}

# links
bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'

# ---       FUNCTIONS        ---#


def icons():
    counter = 0
    for png in soup.findAll('img'):
        coin_links[counter] = png.get('src')
        counter += 1

    counter2 = 10
    counter3 = 0
    while counter2 < 60:
        coin_icons[counter3] = coin_links[counter2]
        counter2 += 1
        counter3 += 1


def name():
    counter = 0
    for name in soup.find_all('div', class_='tbl-currency'):
        name = name.text
        clean_name = unicodedata.normalize("NFKD", name)
        clean_name = clean_name.strip()
        clean_name = clean_name.replace('\n', '')
        coin_names[counter] = clean_name
        counter += 1


def percent():
    counter = 0
    for percent in soup.find_all('td', class_='tbl-col-md change-period clickable-coin-td'):
        percent = percent.text
        clean_percent = unicodedata.normalize("NFKD", percent)
        clean_percent = clean_percent.rstrip()
        coin_percent[counter] = clean_percent
        counter += 1


def prices():
    clean_prices = {}

    counter = 0
    for price in soup.find_all('td', class_='clickable-coin-td'):
        price = price.text
        clean_price = unicodedata.normalize("NFKD", price)
        clean_price = clean_price.strip('')
        clean_price = clean_price.replace('\n', '')
        if clean_price.find('Mkt') != -1 or clean_price.find('%') != -1 or clean_price.find('M') != -1 \
                or clean_price.find('B') != -1 or clean_price.find('K') != -1 or clean_price.find('LEO') != -1:
            pass
        else:
            clean_price = clean_price.replace('฿', ' \n฿')
            clean_price = clean_price.replace('$', '$ ')
            clean_price = clean_price.replace('USDC', ' \nUSDC')
            clean_price = clean_price.replace('ETH', ' \nETH')
            clean_price = clean_price.replace('DAI', ' \nDAI')
            clean_price = clean_price.replace('$ 1ERD  46', '')
            clean_prices[counter] = clean_price
            counter += 1

    # Creates a new dict removing all the blank keys from 'clean_prices'
    counter2 = 0    # Checks dict for even #'s and adds them to the new dict
    counter3 = 0    # New dict starting from '0'
    for price in clean_prices:
        if price % 2 == 1:
            coin_prices[counter3] = clean_prices[counter2]
            counter2 += 1
            counter3 += 1
        else:
            counter2 += 1

# ---       MAIN LINE       ---#


class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def bot_spam_channel_check(self):
        botspam_channels = 667538928512794644
        # 667538928512794644: Ignium's Server - #bot-spam
        if botspam_channels == self.bot.get_channel(667538928512794644):
            return botspam_channels

    @commands.command()
    @commands.check(bot_spam_channel_check)
    async def crypto(self, ctx, coin_number):
        name()
        icons()
        prices()
        percent()
        emoji_list = ['◀', '▶']

        embed = discord.Embed(
            title=str(coin_prices.get(int(coin_number) + (-1))),
            description=' ',
            colour=discord.Colour.blurple()
        )
        embed.set_footer(text=site)
        if 0 < int(coin_number) <= 50:
            embed.set_author(
                name=f'{coin_number}. {str(coin_names.get(int(coin_number) + (-1)))}',
                icon_url=f'https://coinlib.io/{str(coin_icons.get(int(coin_number) + (-1)))}'
            )
            embed.add_field(name='24 Hour Change', value=str(coin_percent.get(int(coin_number) + (-1))), inline=False)
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
    @commands.check(bot_spam_channel_check)
    async def cryptolist(self, ctx, page):
        name()
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
            counter = 0
            while counter < 10:
                embed.add_field(name=f'{counter + 1}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '2':
            counter = 10
            while counter < 20:
                embed.add_field(name=f'{counter + 1}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '3':
            counter = 20
            while counter < 30:
                embed.add_field(name=f'{counter + 1}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '4':
            counter = 30
            while counter < 40:
                embed.add_field(name=f'{counter + 1}. {str(coin_names.get(counter))}',
                                value=str(coin_prices.get(counter)),
                                inline=False)
                counter += 1
        elif page == '5':
            counter = 40
            while counter < 50:
                embed.add_field(name=f'{counter + 1}. {str(coin_names.get(counter))}',
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
