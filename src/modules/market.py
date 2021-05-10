# ---       IMPORTS          --- #
import datetime

import discord
import json
import os
import psycopg2
import schedule
import time

from psycopg2 import errors

from discord.ext import commands
from dotenvy import load_env, read_file
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# ---       LINKS        --- #
coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'

# ---       LOAD API         --- #

load_env(read_file('../../.env'))
API_KEY = os.environ.get('CMC_API_KEY')
DB_DEV_PW = os.environ.get('DB_DEV_PW')

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

session = Session()
session.headers.update(headers)

# ---       API PARAMS        --- #
coin_parameters = {  # Retrieves coins listed 1-50
    'start': '1',
    'limit': '50',
    'convert': 'USD'
}

# ---       CONNECT TO DB       --- #

con = psycopg2.connect(
    host='localhost',
    database='PyBo_Local',
    user='postgres',
    password=DB_DEV_PW
)

# ---        INIT DATA IN DB        --- #


def cache_coins():
    try:
        cur = con.cursor()
        coin_response = session.get(coin_url, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data['data']

        for x in coins:
            id = x['id']
            name = x['name']
            symbol = x['symbol']
            price = x['quote']['USD']['price']

            cur.execute("INSERT INTO coin_info (coin_id, coin_name, coin_symbol, coin_price)"
                        "VALUES (%s, %s, %s, %s)", (id, name, symbol, price))
            con.commit()  # Commit transaction

            cur.close()  # Close cursor
            con.close()  # Close connection
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

# ---       UPDATE DATA IN DB       --- #


def update_coins():
    try:
        cur = con.cursor()
        TNOW = datetime.datetime.now().replace(microsecond=0)
        coin_response = session.get(coin_url, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data['data']

        for x in coins:
            id = x['id']
            price = x['quote']['USD']['price']

            cur.execute("UPDATE coin_info "
                        "SET coin_price = %s "
                        "WHERE coin_id = %s ",
                        (price, id))

            con.commit()  # Commit transaction
        print(f'{TNOW}: Updates data every minute')
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# ---     CUSTOM CHECKS     --- #


def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       ---#

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


#     @commands.command()
#     @commands.check(bot_channel_check)
#     async def crypto(self, ctx, coin_number):
#         # Function calls
#         abbreviations()
#         names()
#         icons()
#         prices()
#         percent_change()
#         # Variables
#         emoji_list = ['◀', '▶']
#         coin_number = int(coin_number)
#
#         embed = discord.Embed(
#             title=str(coin_prices.get(coin_number)),
#             description=' ',
#             colour=discord.Colour.blurple()
#         )
#         embed.set_footer(text=site)
#         if 0 < int(coin_number) <= 10:
#             embed.set_author(
#                 name=f'{coin_number}. {str(coin_names.get(coin_number))} / {str(coin_abbreviation.get(coin_number))}',
#                 icon_url=coin_icons.get(int(coin_number))
#             )
#             embed.add_field(name='24h % Change', value=str(coin_percent_change.get(coin_number)), inline=False)
#         elif 11 <= int(coin_number) <= 50:
#             embed.set_author(
#                 name=f'{coin_number}. {str(coin_names.get(coin_number))} / {str(coin_abbreviation.get(coin_number))}'
#             )
#             embed.add_field(name='24h % Change', value=str(coin_percent_change.get(coin_number)), inline=False)
#         else:
#             embed = discord.Embed(
#                 title='Invalid Number',
#                 description=' ',
#                 colour=discord.Colour.red()
#             )
#
#         message_embed = await ctx.send(embed=embed)
#         for emoji in emoji_list:
#             await message_embed.add_reaction(emoji)
#
#         if message_embed.on_raw_reaction_add() == emoji_list:
#             print('test')
#
#     @commands.command()
#     @commands.check(bot_channel_check)
#     async def cryptolist(self, ctx, page):
#         # Function Calls
#         abbreviations()
#         names()
#         prices()
#         # Variables
#         # emoji_list = ['◀', '▶']
#         page = int(page)
#
#         embed = discord.Embed(
#             title=' ',
#             description=' ',
#             colour=discord.Colour.blurple()
#         )
#
#         embed.set_author(name=f'Top {10 * page} Crypto Coins',
#                          icon_url=bot_avatar_link)
#         embed.set_footer(text=site)
#
#         if page == 1:
#             counter = 1
#             while counter < 11:
#                 embed.add_field(name=f'{counter}. {str(coin_names.get(counter))} / {str(coin_abbreviation.get(counter))}',
#                                 value=str(coin_prices.get(counter)),
#                                 inline=False)
#                 counter += 1
#         elif page == 2:
#             counter = 11
#             while counter < 21:
#                 embed.add_field(name=f'{counter}. {str(coin_names.get(counter))} / {str(coin_abbreviation.get(counter))}',
#                                 value=str(coin_prices.get(counter)),
#                                 inline=False)
#                 counter += 1
#         elif page == 3:
#             counter = 21
#             while counter < 31:
#                 embed.add_field(name=f'{counter}. {str(coin_names.get(counter))} / {str(coin_abbreviation.get(counter))}',
#                                 value=str(coin_prices.get(counter)),
#                                 inline=False)
#                 counter += 1
#         elif page == 4:
#             counter = 31
#             while counter < 41:
#                 embed.add_field(name=f'{counter}. {str(coin_names.get(counter))} / {str(coin_abbreviation.get(counter))}',
#                                 value=str(coin_prices.get(counter)),
#                                 inline=False)
#                 counter += 1
#         elif page == 5:
#             counter = 41
#             while counter < 51:
#                 embed.add_field(name=f'{counter}. {str(coin_names.get(counter))} / {str(coin_abbreviation.get(counter))}',
#                                 value=str(coin_prices.get(counter)),
#                                 inline=False)
#                 counter += 1
#
#         message_embed = await ctx.send(embed=embed)
#         # for emoji in emoji_list:
#         #     await message_embed.add_reaction(emoji)
#
#     @crypto.error
#     async def crypto_error(self, ctx, error):
#         if isinstance(error, commands.MissingRequiredArgument):
#             embed = discord.Embed(
#                 title='Error: Specify crypto #',
#                 description=' ',
#                 colour=discord.Colour.red()
#             )
#             embed.set_footer(text='ex => ;crypto 1')
#
#             await ctx.send(embed=embed, delete_after=5)
#
#     @cryptolist.error
#     async def cryptolist_error(self, ctx, error):
#         if isinstance(error, commands.MissingRequiredArgument):
#             embed = discord.Embed(
#                 title='Error: Specify cryptolist #',
#                 description=' ',
#                 colour=discord.Colour.red()
#             )
#             embed.set_footer(text='ex => ;cryptolist 1')
#
#             await ctx.send(embed=embed, delete_after=5)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Market(bot))


# ---       CACHES DATA IN DB        ---#
schedule.every(1).minutes.do(update_coins)
while True:
    schedule.run_pending()
    time.sleep(1)

