import discord
from sakuraiembed import embedwriter

name = 'latency'
description = 'Shows the current API latency'
usage = '>latency'
category = 'meta'

async def plugin_main(client, message, config):
	embed = embedwriter(config, message)
	await embed.send_embed("API latency", "{}ms".format(round(client.latency, 1)*100), 0x110011)