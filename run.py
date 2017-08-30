import discord
import embedwriter
import os
import sys
from discord.ext import commands

description = ''' Sakurai_Bot '''
bot = commands.Bot(command_prefix=">", description=description)
embed = embedwriter.embedwriter(bot)
version = '0.1'
owner_id = '[owner id]'
plugins = []
sys.path.append("plugins/")

@bot.event
async def on_ready():
    print("Sakurai connected.")
    await bot.change_presence(game=discord.Game(name=str(len(bot.servers)) + ' servers'))

@bot.event
async def on_message(message):
    if message.content.startswith(">"):
        if message.content.startswith(">help"):
            if message.content == ">help":
                description = 'List of available commands:\n'
                for plugin in plugins:
                    description += '`%s`,  ' % plugin
                    description = description[:-1]
                await embed.send_embed(message.channel, "Help", description, 0xdbfeb8)
            else:
                command = message.content.replace(">help ", "")
                plugin = load_plugin(command)
                description = 'Command `%s`\nDescription: *%s*\nUsage: `%s`' % (command, plugin.description, plugin.usage)
                await embed.send_embed(message.channel, ">" + command, description, 0xdbfeb8)
        else:
            if any(message.content[1:].split()[0] in s for s in plugins):
                await call_plugin(message.content[1:].split()[0], message.channel, message)


# PLUGIN LOADER #

def load_plugin(name):
    mod = __import__("%s-plugin" % name)
    return mod

async def call_plugin(name, channel, message):
    plugin = load_plugin(name)
    await plugin.plugin_main(channel, bot, message)

for file in os.listdir("plugins/"):
    if file.endswith("-plugin.py"):
        print("Loading plugin " + file.replace("-plugin.py", "") + "...")
        plugins.append(file.replace("-plugin.py", ""))

bot.run('[your token]')
