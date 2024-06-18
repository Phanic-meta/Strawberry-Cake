import re
from discord import app_commands


def check_admin(message):
    if message.author.guild_permissions.administrator:
        return True
    else:
        return False


def emoji_getter(interaction, current):
    emojis = []
    x = str(interaction.guild.emojis)
    id = re.findall("[0-9]+", x)
    name = re.findall("(?<==')(.*?)(?=\')", x)
    for i in range(len(interaction.guild.emojis)):
        if current.lower() in name[i].lower():
            emojis.append(app_commands.Choice(name=f':{name[i]}:', value=f'<:{name[i]}:{id[i]}>'))
    return emojis
