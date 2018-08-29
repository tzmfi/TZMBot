# my discord bot for TZM discord

import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='-')
client.remove_command("help")

extensions = ["role_reactions"]


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="with the concept of real socialism"))
    print("I exist now!")
    print("i'm running on {} with the ID: {}.".format(client.user.name, client.user.id))

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

    token = "" # Bot token removed for security purposes
    client.run(token)
