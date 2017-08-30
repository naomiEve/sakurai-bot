#Example of a simple plugin

#always, ALWAYS import discord. embedwriter is necessary only if you want to use embeds.
import discord
import embedwriter

#IMPORTANT! PLUGIN INFORMATION#
name = 'echo'
description = 'Echoes whatever you say to the bot'
usage = '>echo <message>'

#main function, HAS to be async.
async def plugin_main(channel, bot, message):
    embed = embedwriter.embedwriter(bot) #create an embedwriter instance
    await embed.send_embed(channel, "Echo!", message.content.replace(">echo ", ""), 0xdbfeb8)
