##############
# sakuraiembed, part of sakurai2 - (c) prefetcher 2018

import discord

class embedwriter():
	def __init__(self, config, message=None):
		self.config = config
		if message:
			self.message = message

	def set_message(self, message):
		self.message = message

	async def send_embed(self, title, description, colour, footer='', image=None, thumb=None, footerImage=None):
		await self.message.channel.trigger_typing()
		embed = discord.Embed(title=title, description=description, colour=colour)
		if image is not None:
			embed.set_image(url=image)
		if thumb is not None:
			embed.set_thumbnail(url=thumb)
		if footer == '' and footerImage == None:
			embed.set_footer(text="Sakurai " + self.config["version"] + " | requested by " + self.message.author.name, icon_url=self.message.author.avatar_url)
		else:
			if footerImage:
				embed.set_footer(text=footer, icon_url=footerImage)
			else:   
				embed.set_footer(text=footer)

		await self.message.channel.send(embed=embed)
