##############
# sakurai2 - (c) prefetcher 2018

import discord
import json
import sys, os, tempfile

sys.path.append("./plugins/")
sys.path.append("./utils")

from sakuraiembed import embedwriter
from discordbots import api

# local variables
plugins = []
with open('config.json') as config_raw:
    config = json.load(config_raw)

# Drop the pidfile (i.e. if you'd want to monitor it using monit)
pid = str(os.getpid())
filedir = tempfile.gettempdir() + "/sakurai.pid" # Cross-platform solution
open(filedir, 'w').write(pid)

# Sakurai code
class Sakurai(discord.Client):
	def attach_config(self, config):
		self.config = config

	def attach_plugins(self, plugins):
		self.plugins = plugins

	async def on_ready(self):
		await self.change_presence(game=discord.Game(name=self.config['default_prefix'] + "help | " + str(len(self.guilds)) + " guilds", type=3))
		if config["discordbots_api"]["enabled"]:
			self.dbapi = api(self.user.id, config["discordbots_api"]["bot_token"])
		print('Sakurai Connected!')
		print('Username: {0.name}\nID: {0.id}'.format(self.user))
		print(self.config)

	async def on_message(self, message):
		if message.content.startswith(config['default_prefix']) and not message.author.bot:
			embed = embedwriter(config, message)
			cmd = message.content.split(' ')[0].replace(config['default_prefix'], "") # Get the command invoked
			if cmd in self.plugins: # Is the command a plguin?
				print(message.author.name + ": " + message.content)
				if cmd == "help": # Is the command "help"?
					if message.content == config['default_prefix'] + "help": # Does the command have no parameters?
						description = 'To get help about a command, type `' + config['default_prefix'] + 'help <command>`\n\n'
						plugindata = {}
						for plugin in plugins:
							loaded_plugin = load_plugin(plugin)
							if not loaded_plugin.category in plugindata: # If the category doesn't exist, create it.
								plugindata[loaded_plugin.category] = []
							plugindata[loaded_plugin.category].append(loaded_plugin.name) # Add the plugin to the category
						for category in plugindata.keys():
							description += "**" + category.title() + "**\n" # Add a new section with the category
							for item in plugindata[category]:
								description += "`" + item + "`, " # Add every plugin from the category to the section
							description = description[:-2]
							description += "\n\n"
						await embed.send_embed("List of available commands", description, 0xdbfeb8, '', None, self.user.avatar_url)
					else:
						command = message.content.replace(config['default_prefix'] + "help ", "")
						plugin = load_plugin(command)
						description = 'Command `%s`\nDescription: *%s*\nUsage: `%s`' % (command, plugin.description, plugin.usage)
						await embed.send_embed(config['default_prefix'] + command, description, 0xdbfeb8)
				else:
					await call_plugin(cmd, self, message, self.config)
			else:
				print("[INFO] Command not found.")

		async def on_guild_join(self, server):
			if config["discordbots_api"]["enabled"]:
				self.dbapi.update_servers(len(self.guilds))

		async def on_guild_remove(self, server):
			if config["discordbots_api"]["enabled"]:
				self.dbapi.update_servers(len(self.guilds))

# PLUGIN LOADER #

def load_plugin(name):
    mod = __import__("%s-plugin" % name)
    return mod

async def call_plugin(name, client, message, config):
    plugin = load_plugin(name)
    await plugin.plugin_main(client, message, config)

for file in os.listdir("./plugins/"):
    if file.endswith("-plugin.py"):
        print("Loading plugin " + file.replace("-plugin.py", "") + "...")
        plugins.append(file.replace("-plugin.py", ""))

# Start-up
sakurai = Sakurai()
sakurai.attach_config(config)
sakurai.attach_plugins(plugins)
sakurai.run(config['token'])