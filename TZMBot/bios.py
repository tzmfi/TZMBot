import discord
from discord.ext import commands
import asyncio
import json

from settings import userinfo_location

class bios:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def setbio(self, ctx, *, new_bio: str):
        user = ctx.message.author

        # creates and sends confirmation message:
        embed = discord.Embed(title="Are you sure you want to update your bio to this?",
                              description=new_bio,
                              colour=0x8a0707)
        embed.set_footer(icon_url=user.avatar_url,
                         text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
        confirmation_message = await self.client.send_message(ctx.message.channel, embed=embed)

        # adds emojis for ease of use:
        await self.client.add_reaction(confirmation_message, "🇾")
        await self.client.add_reaction(confirmation_message, "🇳")

        # waits for Yes or No reaction and executes accordingly:
        while True:
            rea = await self.client.wait_for_reaction(message=confirmation_message)

            if rea.user == user:  # makes sure that the user reacting is the user changing their bio
                rea = rea.reaction # if so, we know that the user variable set earlier is the same as rea.user so we can safely set rea to be just the reaction

                # if they confirm the bio change:
                if str(rea.emoji) == "🇾":
                    await self.client.clear_reactions(confirmation_message)

                    # reads the file for editing:
                    with open(userinfo_location, "r") as f:
                        file = json.load(f)

                    # updates the file:
                    found = False  # found defaults to false
                    with open(userinfo_location, "w") as f:

                        # checks if the user already has a bio, and updates it if so:
                        for item in file["users"]:
                            if item["id"] == user.id:
                                found = True  # sets found to true if the user already has a bio
                                item["bio"] = new_bio
                                json.dump(file, f, indent=2, sort_keys=True)

                        # if the script above didn't find an already existant bio for the user, this creates a new one from scratch:
                        if not found:
                            new_user = {
                                "bio": "{}".format(new_bio),
                                "id": "{}".format(user.id)}
                            file["users"].append(new_user)
                            json.dump(file, f, indent=2, sort_keys=True)

                        # edits the confirmation message to clarify that the user's bio has been set/updated:
                        embed = discord.Embed(title="Bio update confirmed",
                                              colour=0x8a0707)
                        embed.set_footer(icon_url=user.avatar_url,
                                         text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
                        await self.client.edit_message(confirmation_message, embed=embed)

                        print("Updated bio for {}#{} to: [{}]".format(user.name, user.discriminator, new_bio))
                        break

                # if they cancel the bio change:
                elif str(rea.emoji) == "🇳":
                    await self.client.clear_reactions(confirmation_message)

                    # edits the confirmation message to clarify that the bio change/creation has been cancelled:
                    embed = discord.Embed(title="Bio update cancelled",
                                          colour=0x8a0707)
                    embed.set_footer(icon_url=user.avatar_url,
                                     text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
                    await self.client.edit_message(confirmation_message, embed=embed)
                    break

    @commands.command(pass_context=True)
    async def bio(self, ctx, *target_user):
        user = ctx.message.author

        # figures out who to target/explains the issue if there's improper inout:
        while True:
            if len(target_user) == 0:
                target_user = user
            else:
                if len(ctx.message.mentions) == 0:
                    embed = discord.Embed(title="Please try again.",
                                          description="Please mention the user you want to check the bio of.",
                                          colour=0x8a0707)
                    embed.set_footer(icon_url=user.avatar_url,
                                     text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
                    await self.client.send_message(ctx.message.channel, embed=embed)
                    break
                elif len(ctx.message.mentions) == 1:
                    target_user = ctx.message.mentions[0]
                else:
                    embed = discord.Embed(title="Please try again.",
                                          description="Please mention only one user per command.",
                                          colour=0x8a0707)
                    embed.set_footer(icon_url=user.avatar_url,
                                     text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
                    await self.client.send_message(ctx.message.channel, embed=embed)
                    break

            # reads the file:
            with open(userinfo_location, "r") as f:
                file = json.load(f)

            # searches for whether the targeted user has a bio, and sets it to the bio variable if so
            found = False
            for item in file["users"]:
                if item["id"] == target_user.id:
                    bio = item["bio"]
                    found = True

            # create embed for if a bio was found for the user:
            if found:
                embed = discord.Embed(title="Here's {}'s bio".format(target_user.name),
                                      description=bio,
                                      colour=0x8a0707)
                embed.set_thumbnail(url=target_user.avatar_url)
                embed.set_footer(icon_url=user.avatar_url,
                                 text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
            # creates embed for if a bio was not found for the user:
            elif not found:
                embed = discord.Embed(title="{} hasn't set a bio.".format(target_user.name),
                                      description="This user hasn't set a bio yet",
                                      colour=0x8a0707)
                embed.set_thumbnail(url=target_user.avatar_url)
                embed.set_footer(icon_url=user.avatar_url,
                                 text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
            await self.client.send_message(ctx.message.channel, embed=embed)
            break

def setup(client):
    client.add_cog(bios(client))
