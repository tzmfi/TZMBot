# my discord bot for TZM discord

import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='-')
client.remove_command("help")

extensions = []


async def role_reactions():
    channel = client.get_channel("480735329565802505")  # gets channel to run in

    # deletes all previous messages in channel:
    old_messages = []
    async for m in client.logs_from(channel, limit=500):
        old_messages.append(m)
    if len(old_messages) >= 2:
        await client.delete_messages(old_messages)
    elif len(old_messages) == 1:
        old_message = old_messages[0]
        await client.delete_message(old_message)

    # creates and sends message for reactions creation:
    embed = discord.Embed(title="Chapter categories", description="There are other categories in this server for specific chapter channels such as the example in the top right corner of this message", colour=0x8a0707)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/474667856206888983/479615723078156288/download.png")
    embed.add_field(name="React to this message with one of the below country flag emojis to get access to the corresponding category. Don't forget that you can remove your access to categories by reacting again with the same emoji.", value=":flag_au: - Autstrailia\n:flag_us: - USA\n...")
    embed.set_footer(text="Created by CHATALOT1", icon_url="https://cdn.discordapp.com/avatars/353574266236567556/ef9d8fa7b54d8f8c58b3f81b6071b087")
    message = await client.send_message(channel, embed=embed)

    # loop for managing roles and reactions:
    while True:
        # waits for a reaction then sets variables for the member who added the reaction and the reaction itself:
        rea = await client.wait_for_reaction(message=message)  # waits for a reaction to be added then outputs a namedtuple containing the reaction and the user who added it
        user = rea.user
        rea = rea.reaction

        # checks for specific reactions then adds or removes the corresponding role accordingly:
        if str(rea.emoji) == "🇦🇺":
            role = discord.utils.get(user.server.roles, id="481854045623943179")
            if "481854045623943179" in [r.id for r in user.roles]:
                await client.remove_roles(user, role)
                await client.send_message(user, content="removed the {} role!".format(role))
                await client.clear_reactions(message)
                print("took {} role from {}#{}".format(role.name, user.name, user.discriminator))
            else:
                await client.add_roles(user, role)
                await client.send_message(user, content="gave you the {} role!".format(role))
                await client.clear_reactions(message)
                print("gave {} role to {}#{}".format(role.name, user.name, user.discriminator))
        elif str(rea.emoji) == "🇺🇸":
            role = discord.utils.get(user.server.roles, id="481854115920478227")
            if "481854115920478227" in [r.id for r in user.roles]:
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
    chat = await client.get_user_info("353574266236567556")
    await client.say(
        "I am a bot developed by {}. So far my only feature of any worth is the reaction based role assigning system that allows you to view other categories."
            .format(chat.mention))


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

    token = ""
    client.run(token)
