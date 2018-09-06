# my discord bot for TZM discord

import discord
from discord.ext import commands
import asyncio
import os

from settings import role_ids 
from settings import channel_id

client = commands.Bot(command_prefix='-')
client.remove_command("help")

extensions = ["bios"]

async def role_reactions():
    channel = client.get_channel(channel_id)  # gets channel to run in
    
    # deletes all previous messages in channel:
    old_messages = []
    async for m in client.logs_from(channel, limit=500):
        if m.author == client.user:
            old_messages.append(m)
    if len(old_messages) >= 2:
        await client.delete_messages(old_messages)
    elif len(old_messages) == 1:
        old_message = old_messages[0]
        await client.delete_message(old_message)

    # converts role_ids into a string for the reactions message:
    role_reactions_string = ""
    for item in role_ids:
        role = discord.utils.get(channel.server.roles, id=role_ids[item])
        if role is not None:
            role_reactions_string = role_reactions_string + "\n" + item + " - " + role.mention
        else:
            print("Invalid role_id {}:{}".format(item, role_ids[item]))
            
    if len(role_reactions_string) == 0:
            role_reactions_string = "empty"

    # creates and sends message for reactions creation:
    embed = discord.Embed(title="Chapter categories",
                          description="There are other categories in this server for specific chapter channels such as the example in the top right corner of this message",
                          colour=0x8a0707)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/474667856206888983/479615723078156288/download.png")
    embed.add_field(name="React to this message with one of the below country flag emojis to get access to the corresponding category. Don't forget that you can remove your access to categories by reacting again with the same emoji.",
                    value=role_reactions_string)
    embed.set_footer(text="Created by CHATALOT1", icon_url="https://cdn.discordapp.com/avatars/353574266236567556/ef9d8fa7b54d8f8c58b3f81b6071b087")
    message = await client.send_message(channel, embed=embed)

    # loop for managing roles and reactions:
    while True:
        # waits for a reaction then sets variables for the member who added the reaction and the reaction itself:
        rea = await client.wait_for_reaction(message=message)  # waits for a reaction to be added then outputs a namedtuple containing the reaction and the user who added it
        user = rea.user
        rea = rea.reaction

        # checks for specific reactions then adds or removes the corresponding role accordingly:
        if str(rea.emoji) in role_ids:
            role_id = role_ids[str(rea.emoji)]
            role = discord.utils.get(user.server.roles, id=role_id)
            if role is None:
                print("Invalid reaction added by {}#{}: {}".format(user.name, user.discriminator, rea.emoji))
            elif role_id in [r.id for r in user.roles]:
                await client.remove_roles(user, role)
                await client.send_message(user, content="removed the {} role!".format(role))
                await client.clear_reactions(message)
                print("took {} role from {}#{}".format(role.name, user.name, user.discriminator))
            else:
                await client.add_roles(user, role)
                await client.send_message(user, content="gave you the {} role!".format(role))
                await client.clear_reactions(message)
                print("gave {} role to {}#{}".format(role.name, user.name, user.discriminator))
        # if the reaction is none of the above, removes the reaction and prints some info to the console:
        else:
            await client.clear_reactions(message)
            print("Invalid reaction added by {}#{}: {}".format(user.name, user.discriminator, rea.emoji))


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="with the concept of real socialism"))
    print("I exist now!")
    print("i'm running on {} with the ID: {}.".format(client.user.name, client.user.id))
    await role_reactions()


@client.command(pass_context=True)
async def info(ctx):
    user = ctx.message.author
    chat = await client.get_user_info("353574266236567556")
    jeukku = await client.get_user_info("333945749803106306")

    embed = discord.Embed(title="TZMBot info:",
                          description="All sorts of info about me!",
                          colour=0x8a0707)
    embed.add_field(name="Developed by:",
                    value="I am developed mainly by {}, with help from {}.".format(chat.mention, jeukku.mention))
    embed.add_field(name="Features:",
                    value="Currently my only features are the role reactions system and the bio system (do -help for more info)")
    embed.add_field(name="Technical stuff:",
                    value="**Programming language:** Python 3.6\n**Library:** discord.py 0.16.2\n**Fuel:** dreams (of an RBE)")
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(icon_url=user.avatar_url,
                     text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
    await client.send_message(ctx.message.channel, embed=embed)


@client.command(pass_context=True)
async def help(ctx):
    user = ctx.message.author
    role_reactions_channel = client.get_channel(channel_id)

    embed = discord.Embed(title="TZMBot help:",
                          description="How to use me!",
                          colour=0x8a0707)
    embed.add_field(name="The role reactions system:",
                    value="The role reactions system is the name of the setup you see in {}, it explains itself pretty well over there."
                    .format(role_reactions_channel.mention))
    embed.add_field(name="The bio system:",
                    value="""The bio system is designed as a way to easily explain to others what you can do and have done for TZM, it consists of:
                    
                    ``-setbio [new bio]`` - This command will update your bio to whatever you put in place of ``[new bio]``.
                    ``-bio {user}`` = This command will display the bio of the user you @mention in place of ``{user}``. Alternatively, if you put nothing after the command, it will display your own bio by default.""")
    embed.add_field(name="Misc.",
                    value="""``-info`` - Displays info about me.
                    ``-help`` - Displays this message.""")
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(icon_url=user.avatar_url,
                     text="Requested by {}#{} ({})".format(user.name, user.discriminator, user.id))
    await client.send_message(ctx.message.channel, embed=embed)

    
@client.command(pass_context=True)
async def load(ctx, extension):
    if ctx.message.author.id == "353574266236567556":
        try:
            client.load_extension(extension)
            print("loaded {}".format(extension))
            await client.say("{} loaded".format(extension))
        except Exception as error:
            print("{} can not be loaded. [{}]".format(extension, error))


@client.command(pass_context=True)
async def unload(ctx, extension):
    if ctx.message.author.id == "353574266236567556":
        try:
            client.unload_extension(extension)
            print("unloaded {}".format(extension))
            await client.say("{} unloaded".format(extension))
        except Exception as error:
            print("{} can not be unloaded. [{}]".format(extension, error))


if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    token = os.environ['TZMBOT_TOKEN']
    client.run(token)
