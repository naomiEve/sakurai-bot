import discord

class embedwriter():
    def __init__(self, bot):
        self.bot = bot

    async def send_embed(self, channel, title, description, colour, footer='', image=None):
        embed = discord.Embed(title=title, description=description, colour=colour)
        if image:
            embed.set_image(url=image)

        embed.set_footer(text=footer)
        await self.bot.send_message(channel, embed=embed)
