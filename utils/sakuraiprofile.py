import sqlite3
import time
import json

class sakuraiprofile():
	def __init__(self, tag):
		self.stdxp = 150
		self.tag = tag
		self.db = db = sqlite3.connect("./sakurai.db")

	def does_user_exist(self, tag=None):
		cursor = self.db.cursor()
		if tag is None:
			tag = self.tag

		cursor.execute("SELECT * FROM profiles WHERE id = ?", (tag,))
		user = cursor.fetchone()
		if user is None:
			return False
		else:
			return True

	def create_user(self, tag=None):	
		cursor = self.db.cursor()
		if tag is None:
			tag = self.tag

		cursor.execute("INSERT INTO profiles (id) VALUES (?)", (tag,))
		self.db.commit()

	def get_user_info(self, tag=None):
		cursor = self.db.cursor()
		if tag is None:
			tag = self.tag

		cursor.execute("SELECT * FROM profiles WHERE id = ?", (tag,))
		user = cursor.fetchone()
		userdata = {"id": user[0], "desc": user[1], "lvl": user[2], "xp": user[3], "coins": user[4], "rep": user[5], "last_coin_retrieve": user[6], "last_rep": user[7], "badges": user[8]}
		return userdata

	def check_last_rep(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT strftime('%s', last_rep_give) FROM profiles WHERE id = ?", (self.tag,))
		user = cursor.fetchone()
		return int(user[0])

	def check_last_payout(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT strftime('%s', last_coin_retrieve) FROM profiles WHERE id = ?", (self.tag,))
		user = cursor.fetchone()
		return int(user[0])	

	def check_lvl(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT xp, lvl FROM profiles WHERE id = ?", (self.tag,))
		data = cursor.fetchone()
		next_lvl_points = round(self.stdxp + data[1] * self.stdxp + (data[1] * self.stdxp) / 2)
		if data[0] >= next_lvl_points:
			cursor.execute("UPDATE profiles SET lvl = lvl + 1 WHERE id = ?", (self.tag,))
			self.db.commit()
			self.give_coins(15)

	def give_xp(self, amount):
		cursor = self.db.cursor()
		cursor.execute("UPDATE profiles SET xp = xp + ? WHERE id = ?", (amount, self.tag))
		self.db.commit()
		self.check_lvl()

	def give_coins(self, amount, tag=None):
		cursor = self.db.cursor()
		if tag is None:
			tag = self.tag
		cursor.execute("UPDATE profiles SET coins = coins + ? WHERE id = ?", (amount, tag))
		self.db.commit()

	def set_desc(self, desc):
		cursor = self.db.cursor()
		cursor.execute("UPDATE profiles SET description = ? WHERE id = ?", (desc, self.tag))
		self.db.commit()	

	def payout(self):
		cursor = self.db.cursor()
		if int(time.time()) - self.check_last_payout() > 86400:
			cursor.execute("UPDATE profiles SET coins = coins + 100 WHERE id = ?", (self.tag,))
			cursor.execute("UPDATE profiles SET last_coin_retrieve = CURRENT_TIMESTAMP WHERE id = ?", (self.tag,))
			self.db.commit()
			return True
		else:
			return False

	def send_coins(self, tag, amount):
		cursor = self.db.cursor()
		cursor.execute("UPDATE profiles SET coins = coins + ? WHERE id = ?", (amount, tag))
		cursor.execute("UPDATE profiles SET coins = coins - ? WHERE id = ?", (amount, self.tag))
		self.db.commit()

	def give_rep(self, tag):
		cursor = self.db.cursor()
		if tag == self.tag:
			return False
		if int(time.time()) - self.check_last_rep() > 86400:
			cursor.execute("UPDATE profiles SET rep = rep + 1 WHERE id = ?", (tag,))
			cursor.execute("UPDATE profiles SET last_rep_give = CURRENT_TIMESTAMP WHERE id = ?", (self.tag,))
			self.db.commit()
			return True
		else:
			return False

	def add_badge(self, badge):
		cursor = self.db.cursor()
		cursor.execute("SELECT badges FROM profiles WHERE id = ?", (self.tag,))
		badges = cursor.fetchone()[0]
		decoded = json.loads(badges)
		decoded.append(badge)
		badges = json.dumps(decoded)

		cursor.execute("UPDATE profiles SET badges = ? WHERE id = ?", (badges, self.tag))
		self.db.commit()

	def get_badges(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT badges FROM profiles WHERE id = ?", (self.tag,))
		badges = cursor.fetchone()[0]
		return json.loads(badges)

	def can_buy(self, amount):
		cursor = self.db.cursor()
		cursor.execute("SELECT coins FROM profiles WHERE id = ?", (self.tag,))
		coins = cursor.fetchone()
		if coins[0] >= amount:
			return True
		else:
			return False

	def db_close(self):
		self.db.close()