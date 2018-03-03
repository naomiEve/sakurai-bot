import discord
import os
from sakuraiembed import embedwriter
import datetime
import platform
from uptime import uptime

name = 'info'
description = 'Provides information about the bot'
usage = '>info'
category = 'meta'

async def plugin_main(client, message, config):
    embed = embedwriter(config, message)
    description = '''
**Uptime: %s**\t\t\t\t⚔️ Servers: %s\n
💻 OS: %s\t\t\t\t🌎 discord.py Version: %s\n
''' % (str(datetime.timedelta(seconds=uptime())), str(len(client.guilds)), platform.system() + " " + platform.release(), discord.__version__)
    await embed.send_embed("Sakurai Info", description, 0xdbfeb8, "Sakurai/2.0", "https://78.media.tumblr.com/cabb68c3f4f3e5525d54c37c318945c1/tumblr_nadawiE9m11sj3j7go1_400.gif")
