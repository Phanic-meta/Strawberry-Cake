import typing

import discord
from discord import app_commands

import os
from dotenv import load_dotenv

import Methodes

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f'logged in as {client.user}')


@tree.command(
    name="create",
    description="Create a new Message for Reaction Rolles",
)
async def create(interaction: discord.Interaction, content: str):
    await interaction.response.send_message(content="Reaction Rolles created", ephemeral=True)
    await interaction.channel.send(content)


@tree.command(
    name="add",
    description="Add Reaction Rolles",
)
async def add(interaction: discord.Interaction, emoji: str, message_id: str):
    rMessage = await interaction.channel.fetch_message(message_id)
    if rMessage.author != client.user:
        await interaction.response.send_message(content="You can only add to Messages from Cake", ephemeral=True)
        return
    await rMessage.add_reaction(emoji)
    await interaction.response.send_message(content="Reaction added", ephemeral=True)


@add.autocomplete("emoji")
async def emoji_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    return Methodes.emoji_getter(interaction, current)


@tree.command(
    name="remove",
    description="Remove Reaction Rolles",
)
async def remove(interaction: discord.Interaction, emoji: str, message_id: str):
    rMessage = await interaction.channel.fetch_message(message_id)
    if rMessage.author != client.user:
        await interaction.response.send_message(content="You can only remove from Messages from Cake", ephemeral=True)
        return
    await rMessage.remove_reaction(emoji, member=client.user)
    await interaction.response.send_message(content="Reaction removed", ephemeral=True)


@remove.autocomplete("emoji")
async def emoji_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    return Methodes.emoji_getter(interaction, current)


@client.event
async def on_raw_reaction_add(rawreactionactionevent):
    channel = client.get_channel(rawreactionactionevent.channel_id)
    message = await channel.fetch_message(rawreactionactionevent.message_id)
    for reaction in message.reactions:
        if not reaction.me:
            await reaction.clear()
    if message.author.id != client.user.id:
        return
    if rawreactionactionevent.member.id == client.user.id:
        return
    roles = await message.guild.fetch_roles()
    for role in roles:
        if role.name == rawreactionactionevent.emoji.name:
            await rawreactionactionevent.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(rawreactionactionevent):
    channel = client.get_channel(rawreactionactionevent.channel_id)
    message = await channel.fetch_message(rawreactionactionevent.message_id)

    if message.author.id != client.user.id:
        return
    roles = await message.guild.fetch_roles()

    member = message.guild.get_member(rawreactionactionevent.user_id)
    for role in roles:
        if role.name == rawreactionactionevent.emoji.name:
            await member.remove_roles(role)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not Methodes.check_admin(message):
        await message.reply('You are not an administrator.')
        return

    match message.content.split(" ")[0]:
        case '--sync':
            await tree.sync()
            await message.reply("All have been synced")


client.run(TOKEN)
