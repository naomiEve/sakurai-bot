import requests

class api():
	def __init__(self, cid, token):
		self.id = cid
		self.token = token

	def update_servers(self, count):
		url = "https://discordbots.org/api/bots/" + self.id + "/stats"
		headers = {"Authorization" : self.token}
		payload = {"server_count"  : count}
		requests.post(url, data=payload, headers=headers)
