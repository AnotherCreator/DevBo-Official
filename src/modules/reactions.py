# ---       IMPORTS          ---#
import discord
from discord.ext.commands import Cog


# ---       MAIN LINE       ---#
class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pin_reaction = '👌'
        channel = self.bot.get_channel(798217221934809168)

        if str(reaction.emoji) == pin_reaction:
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

    # TODO: Add a check to see if a user already reacted / added a reaction to a message
        # Method 1: Maybe some sort of array to keep a list of users who reacted
        #           - Then a loop that goes through each index to check if user is in the array
        #           - If user is in array, ignore reaction
        #           - If user is not in array, add the reaction

        # Method 2: A JSON file might be the way to go to temporarily keep track of users who reacted with the message
        #           - Keep a list of users who reacted and add them accordingly
        #           - If a user unreacts to the message remove them from the list
        #           - Once the reaction has reached the threshold, the message cannot be pinned again
        #                   even if all the users unreacted and reacts again

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
