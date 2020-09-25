# ---       IMPORTS          ---#

import discord
from discord.ext.commands import Cog

# ---       GLOBAL VARIABLES          ---#

# ---       FUNCTIONS       ---#

# ---       MAIN LINE       ---#


class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # To get emote format -> \emote
        pin_reaction = '<:lirikWINK:670327394065842207>'
        channel = self.bot.get_channel(746153453075693682)

        if str(reaction.emoji) == pin_reaction:
            print(reaction.count)
            print(f'{user.name} has reacted with {reaction.emoji}')

            pin_count = reaction.count
            if pin_count >= 1:
                embed = discord.Embed(
                    title=reaction.message.content,
                    description=' ',
                    colour=discord.Colour.blurple()
                )
                embed.set_image(
                    url=' '
                )
                embed.set_author(
                    name=reaction.message.author,
                    icon_url=reaction.message.author.avatar_url
                )
                await channel.send(embed=embed)

    '''@Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        print(f'{user.display_name} removed reaction {reaction.emoji}')'''

    '''@Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(f'[RAW] {payload.member.display_name} reacted with {payload.emoji.name}')

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        member = self.bot.guild.get_member(payload.user_id)
        print(f'[RAW] {member.display_name} removed reaction {payload.emoji.name}')'''


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Reactions(bot))