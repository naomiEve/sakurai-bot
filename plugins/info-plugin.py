import discord
import os
import embedwriter
import datetime
import platform
from uptime import uptime

name = 'info'
description = 'Provides information about the bot'
usage = '>info'

async def plugin_main(channel, bot, message):
    embed = embedwriter.embedwriter(bot)
    description = '''
**Uptime: %s**\n
⚔️ Servers: %s\n
💻 OS: %s\n
🌎 discord.py Version: %s\n
''' % (str(datetime.timedelta(seconds=uptime())), str(len(bot.servers)), platform.system(), discord.__version__)
    await embed.send_embed(channel, "Sakurai Info", description, 0xdbfeb8, "Sakurai 0.1", "http://i0.kym-cdn.com/photos/images/original/000/927/575/507.jpg")
