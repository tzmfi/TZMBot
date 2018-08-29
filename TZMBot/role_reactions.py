import discord
from discord.ext import commands
import asyncio

class role_reactions:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def role_reactions(self, ctx):
        if ctx.message.author.id == "353574266236567556":
            # message for reactions creation:
            embed = discord.Embed(title="Chapter categories", description="There are other categories in this server for specific chapter channels such as the example in the top right corner of this message", colour=0x8a0707)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/474667856206888983/479615723078156288/download.png")
            embed.add_field(name="React to this message with one of the below country flag emojis to get access to the corresponding category", value=":flag_au: - Autstrailia\n:flag_us: - USA\n...")
            message = await self.client.send_message(ctx.message.channel, embed=embed)
            await self.client.delete_message(ctx.message)  # deletes command message

            # loop for managing roles and reactions:
            while True:
                # waits for a reaction then sets variables for the member who added the reaction and the reaction itself:
                rea = await self.client.wait_for_reaction(message=message)  # waits for a reaction to be added then outputs a namedtuple containing the reaction and the user who added it
                user = rea.user
                rea = rea.reaction

                # checks for specific reactions then adds or removes the corresponding role accordingly:
                if str(rea.emoji) == "🇦🇺":
                    role = discord.utils.get(user.server.roles, id="481854045623943179")
                    if "481854045623943179" in [r.id for r in user.roles]:
                        await self.client.remove_roles(user, role)
                        await self.client.send_message(user, content="removed the {} role!".format(role))
                        await self.client.clear_reactions(message)
                        print("took {} role from {}#{}".format(role.name, user.name, user.discriminator))
                    else:
                        await self.client.add_roles(user, role)
                        await self.client.send_message(user, content="gave you the {} role!".format(role))
                        await self.client.clear_reactions(message)
                        print("gave {} role to {}#{}".format(role.name, user.name, user.discriminator))
                elif str(rea.emoji) == "🇺🇸":
                    role = discord.utils.get(user.server.roles, id="481854115920478227")
                    if "481854115920478227" in [r.id for r in user.roles]:
                        await self.client.remove_roles(user, role)
                        await self.client.send_message(user, content="removed the {} role!".format(role))
                        await self.client.clear_reactions(message)
                        print("took {} role from {}#{}".format(role.name, user.name, user.discriminator))
                    else:
                        await self.client.add_roles(user, role)
                        await self.client.send_message(user, content="gave you the {} role!".format(role))
                        await self.client.clear_reactions(message)
                        print("gave {} role to {}#{}".format(role.name, user.name, user.discriminator))
                # if the reaction is none of the above, removes the reaction and prints some info to the console:
                else:
                    await self.client.clear_reactions(message)
                    print("Invalid reaction added by {}#{}: {}".format(user.name, user.discriminator, rea.emoji))
        # manages if somebody other then me tries to run the command:
        else:
            chat = await self.client.get_user_info("353574266236567556")
            await self.client.send_message(ctx.message.channel, content="Only {} can use this command!".format(chat.mention))
            print("{}#{} ({}) tried to use role_reactions".format(ctx.message.author.name, ctx.message.author.discriminator, ctx.message.author.id))


def setup(client):
    client.add_cog(role_reactions(client))