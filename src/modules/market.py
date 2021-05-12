# ---       IMPORTS          --- #
import asyncio

import discord
import json
import psycopg2

from collections.abc import Sequence
from discord.ext import commands
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
    'convert': 'USD',
    'aux': 'cmc_rank'
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
            rank = x['cmc_rank']
            name = x['name']
            symbol = x['symbol']
            price = x['quote']['USD']['price']

            cur.execute("INSERT INTO coin_info (coin_id, coin_name, coin_symbol, coin_price, coin_rank)"
                        "VALUES (%s, %s, %s, %s, %s)", (ids, name, symbol, price, rank))
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
            rank = x['cmc_rank']
            price = x['quote']['USD']['price']

            cur.execute("UPDATE coin_info "
                        "SET coin_price = %s, coin_rank = %s "
                        "WHERE coin_id = %s ",
                        (price, rank, id))
            con.commit()  # Commit transaction
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def query_coins(rank):
    cur.execute('SELECT * FROM coin_info ORDER BY coin_rank asc')  # 1,2,3...,100
    rows = cur.fetchall()

    if rank < 11:
        min = 1
        max = 10
    else:
        min = rank - 10
        max = rank
        if max > 100:
            max = 100

    embed = discord.Embed(
        title=' ',
        description=' ',
        colour=discord.Colour.blurple()
    )
    embed.set_footer(text="")

    #  ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Logo: x[4] || Rank: x[5]
    for x in rows:
        if min <= x[5] <= max:
            embed.set_author(name=f'Top {max} Crypto Coins',
                             icon_url=bot_avatar_link)
            embed.add_field(
                name=f'{x[5]}. {x[1]} / {x[2]}',
                value=f'${x[3]}',
                inline=False)
    return embed


def get_left_coin(current_page):
    cur.execute("SELECT * FROM coin_info WHERE coin_rank = %s", (current_page,))
    rows = cur.fetchall()

    # ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Logo: x[4] || Rank: x[5]
    for x in rows:
        embed = discord.Embed(
            title=f'${str(x[3])}',
            description=' ',
            colour=discord.Colour.blurple()
        )
        embed.set_author(
            name=f'{x[5]}. {x[1]} / {x[2]}',
            icon_url=x[4]
        )
        embed.set_footer(text="")
        return embed


def get_right_coin(current_page):
    cur.execute("SELECT * FROM coin_info WHERE coin_rank = %s", (current_page,))
    rows = cur.fetchall()

    # ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Logo: x[4] || Rank: x[5]
    for x in rows:
        embed = discord.Embed(
            title=f'${str(x[3])}',
            description=' ',
            colour=discord.Colour.blurple()
        )
        embed.set_author(
            name=f'{x[5]}. {x[1]} / {x[2]}',
            icon_url=x[4]
        )
        embed.set_footer(text="")
    return embed


# ---     CUSTOM CHECKS     --- #


def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return seq,


def reaction_check(message=None, emoji=None, author=None, ignore_bot=True):
    message = make_sequence(message)
    message = tuple(m.id for m in message)
    emoji = make_sequence(emoji)
    author = make_sequence(author)

    def check(reaction, user):
        if ignore_bot and user.bot:
            return False
        if message and reaction.message.id not in message:
            return False
        if emoji and reaction.emoji not in emoji:
            return False
        if author and user not in author:
            return False
        return True
    return check


# ---       MAIN LINE       ---#

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(bot_channel_check)
    async def coin(self, ctx, *, name):  # Accepts either name or current rank
        # Variables
        emoji_list = ['◀', '▶']

        cur.execute('SELECT * FROM coin_info')
        rows = cur.fetchall()

        await ctx.message.delete()  # Deletes command call
        for x in rows:
            #  ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Logo: x[4] || Rank: x[5]
            if x[1] == name or x[5] == int(name):
                embed = discord.Embed(
                    title=f'${str(x[3])}',
                    description=' ',
                    colour=discord.Colour.blurple()
                )
                embed.set_author(
                    name=f'{x[5]}. {x[1]} / {x[2]}',
                    icon_url=x[4]
                )
                embed.set_footer(text="")
                message = await ctx.send(embed=embed)

                for emoji in emoji_list:
                    await message.add_reaction(emoji)

                check = reaction_check(message=message, author=ctx.author, emoji=(emoji_list[0], emoji_list[1]))
                current_page = x[5]

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
                        if reaction.emoji == emoji_list[0]:  # Left page
                            await message.delete()  # Deletes embed before sending a new one
                            current_page = current_page - 1
                            if current_page <= 0:
                                current_page = 1
                                embed = get_left_coin(1)
                            else:
                                embed = get_left_coin(current_page)
                            message = await ctx.send(embed=embed)

                            for emoji in emoji_list:
                                await message.add_reaction(emoji)

                            check = reaction_check(message=message, author=ctx.author,
                                                   emoji=(emoji_list[0], emoji_list[1]))

                        elif reaction.emoji == emoji_list[1]:  # Right page
                            await message.delete()  # Deletes embed before sending a new one
                            current_page = current_page + 1
                            if current_page >= 100:
                                current_page = 100
                                embed = get_right_coin(100)
                            else:
                                embed = get_right_coin(current_page)
                            message = await ctx.send(embed=embed)

                            for emoji in emoji_list:
                                await message.add_reaction(emoji)

                            check = reaction_check(message=message, author=ctx.author,
                                                   emoji=(emoji_list[0], emoji_list[1]))
                    except TimeoutError:
                        print('Timeout')

    @commands.command()
    @commands.check(bot_channel_check)
    async def top(self, ctx, rank):
        # Variables
        emoji_list = ['◀', '▶']
        rank = int(rank)

        embed = query_coins(rank)

        message_embed = await ctx.send(embed=embed)
        for emoji in emoji_list:
            await message_embed.add_reaction(emoji)

    @coin.error
    async def coin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error: Specify coin rank or name',
                description=' ',
                colour=discord.Colour.red()
            )
            embed.set_footer(text='ex => ;coin 4\nex => ;coin Bitcoin')

            await ctx.send(embed=embed, delete_after=5)

    @top.error
    async def top_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error: Specify top #',
                description=' ',
                colour=discord.Colour.red()
            )
            embed.set_footer(text='ex => ;top 45')

            await ctx.send(embed=embed, delete_after=5)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Market(bot))
