# ---       IMPORTS          ---#
import discord
import psycopg2

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from pybo import DB_DEV_PW, BOT_AVATAR, guild_ids

# ---       CONNECT TO DB       --- #
con = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password=DB_DEV_PW
)
cur = con.cursor()

# ---     CUSTOM CHECKS     --- #
def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       ---#
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Economy(bot))
