# ---       IMPORTS          --- #
import datetime
import discord
import json
import os
import psycopg2
import schedule
import time

from discord.ext import commands
from dotenvy import load_env, read_file
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from pybo import API_KEY, DB_DEV_PW

# ---       LINKS        --- #

api_data = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
api_metadata = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'

# ---       LOAD API         --- #

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

session = Session()
session.headers.update(headers)

# ---       API PARAMS        --- #

coin_parameters = {  # Retrieves coins listed 1-100
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}

# ---       CONNECT TO DB       --- #

con = psycopg2.connect(
    host='localhost',
    database='PyBo_Local',
    user='postgres',
    password=DB_DEV_PW
)
cur = con.cursor()

# ---        DATABASE        --- #


def cache_coins():  # Run this once to init db values
    try:
        id_list = []
        coin_response = session.get(api_data, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data['data']

        for x in coins:
            id_list.append(x['id'])
            ids = x['id']
            name = x['name']
            symbol = x['symbol']
            price = x['quote']['USD']['price']

            cur.execute("INSERT INTO coin_info (coin_id, coin_name, coin_symbol, coin_price)"
                        "VALUES (%s, %s, %s, %s)", (ids, name, symbol, price))
            con.commit()  # Commit transaction

        joined_id = ','.join(map(str, id_list))

        metadata_parameters = {  # Retrieves coin_metadata listed 1-100
            'id': joined_id,
            'aux': 'logo'
        }
        metadata_response = session.get(api_metadata, params=metadata_parameters)
        metadata_data = json.loads(metadata_response.text)
        metadata = metadata_data['data']

        for unique_id in id_list:
            logo_url = metadata[str(unique_id)]['logo']

            cur.execute("UPDATE coin_info "  # Uses UPDATE instead of INSERT since first insertion init coin_logo column
                        "SET coin_logo = %s "
                        "WHERE coin_id = %s ",
                        (logo_url, unique_id))
            con.commit()  # Commit transaction
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def update_coins():
    try:
        coin_response = session.get(api_data, params=coin_parameters)
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

    @commands.command()
    @commands.check(bot_channel_check)
    async def crypto(self, ctx, *, name):
        # Variables
        emoji_list = ['◀', '▶']

        cur.execute('SELECT * FROM coin_info')
        rows = cur.fetchall()

        for x in rows:
            #  ID: x[0]
            #  Name: x[1]
            #  Symbol: x[2]
            #  Price: x[3]
            if x[1] == name:
                embed = discord.Embed(
                    title=x[1],
                    description=' ',
                    colour=discord.Colour.blurple()
                )
                embed.set_footer(text="")
                await ctx.send(embed=embed)
        # if 0 < int(coin_number) <= 10:
        #     embed.set_author(
        #         name=f'{coin_number}. {str(coin_names.get(coin_number))} / {str(coin_abbreviation.get(coin_number))}',
        #         icon_url=coin_icons.get(int(coin_number))
        #     )
        #     embed.add_field(name='24h % Change', value=str(coin_percent_change.get(coin_number)), inline=False)
        # elif 11 <= int(coin_number) <= 50:
        #     embed.set_author(
        #         name=f'{coin_number}. {str(coin_names.get(coin_number))} / {str(coin_abbreviation.get(coin_number))}'
        #     )
        #     embed.add_field(name='24h % Change', value=str(coin_percent_change.get(coin_number)), inline=False)
        # else:
        #     embed = discord.Embed(
        #         title='Invalid Number',
        #         description=' ',
        #         colour=discord.Colour.red()
        #     )

        # for emoji in emoji_list:
        #     await message_embed.add_reaction(emoji)
        #
        # if message_embed.on_raw_reaction_add() == emoji_list:
        #     print('test')

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

# schedule.every(1).minutes.do(update_coins)  # Updates DB every minute
# while True:
#     schedule.run_pending()
#     time.sleep(1)