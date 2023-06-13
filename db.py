import sqlite3


class BotDB():
	"""Connection to database

	   + using
	   -------

	BotDB = BotDB('database_path')"""


	def __init__(self, db_file):
		self.conn = sqlite3.connect(db_file, check_same_thread=False)

		self.cursor = self.conn.cursor()
	def CreateTableUsers(self):
		self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
								id INTEGER PRIMARY KEY AUTOINCREMENT,
								user_id TEXT,
								chat_id TEXT,
								bot_message_language TEXT,
								language_code TEXT,
								message_id TEXT,

								is_bot TEXT,
								first_name TEXT,
								username TEXT,
								role TEXT,

								text STRING,
								type TEXT,
								balance FLOAT,
								reg_date TEXT,
								orders INTEGER,
								UNIQUE (chat_id)
								)''')
	def CreateTablePosts(self):
		self.conn.execute('''CREATE TABLE IF NOT EXISTS posts (
								id INTEGER PRIMARY KEY AUTOINCREMENT,
								user_id TEXT,
								message_id TEXT,
								text TEXT,
								
								model TEXT,
								username TEXT,
								city TEXT,
								description TEXT,
								trade_date TEXT,
								whats_trade INTEGER,
								UNIQUE (message_id)
								)''')

	def AddUser(self, inf_list):
		"""Add user to DataBase

			inf_list
			--------

			+ BotDB.AddUser(user_id, chat_id, bot_message_language, language_code, message_id, is_bot, first_name, username, role, text, type, balance, reg_date, orders)


			+ Defolt values for inf_list:

					+ message_id = message.message_id

					+ username = message.sender_chat.username
 
					+ is_bot = 0
 
					+ language_code = 0
 
					+ chat_id = message.sender_chat.id
 
					+ user_id = message.from_user.id
 
					+ first_name = message.from_user.first_name
 
					+ texts = message.text
 
					+ type1 = message.sender_chat.type
 
					+ bot_message_language = 0
 
					+ balance = 0
 
					+ orders = 0
 
					+ role = None
			
			"""
		try:
			self.cursor.execute("INSERT INTO users (user_id, chat_id, bot_message_language, language_code, message_id, is_bot, first_name, username, role, text, type, balance, reg_date, orders) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", inf_list)
			self.conn.commit()
		except sqlite3.IntegrityError:
			pass #if user is True: pass



	def AddPost(self, inf_list):
		"""same"""
		self.cursor.execute("INSERT INTO posts ('user_id', 'message_id', text, model, username, city, description, trade_date, whats_trade) VALUES(?,?,?,?,?,?,?,?,?)", inf_list)

	def get_post_text(self, user_id):
		result = self.cursor.execute("SELECT text FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_text(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET text = {t} WHERE user_id = {user_id}")
		self.conn.commit()
	
	def get_post_model(self, user_id):
		result = self.cursor.execute("SELECT model FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_model(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET model = {t} WHERE user_id = {user_id}")
		self.conn.commit()
	def get_post_username(self, user_id):
		result = self.cursor.execute("SELECT username FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_username(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET username = {t} WHERE user_id = {user_id}")
		self.conn.commit()

	def get_post_city(self, user_id):
		result = self.cursor.execute("SELECT city FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_city(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET city = {t} WHERE user_id = {user_id}")
		self.conn.commit()
	def get_post_description(self, user_id):
		result = self.cursor.execute("SELECT description FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_description(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET description = {t} WHERE user_id = {user_id}")
		self.conn.commit()
	def get_post_trade_date(self, user_id):
		result = self.cursor.execute("SELECT trade_date FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_trade_date(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET trade_date = {t} WHERE user_id = {user_id}")
		self.conn.commit()
	def get_post_whats_trade(self, user_id):
		result = self.cursor.execute("SELECT whats_trade FROM posts WHERE user_id = ?", (user_id,))
		return result.fetchone()[0]

	def up_post_whats_trade(self, user_id, t):
		self.cursor.execute(f"UPDATE posts SET whats_trade = {t} WHERE user_id = {user_id}")
		self.conn.commit()
	
	def get_AllBuyOnly_model(self):
		result = self.cursor.execute("SELECT model FROM posts")
		return result.fetchall()

	def get_AllBuyOnly_price(self):
		result = self.cursor.execute("SELECT whats_trade FROM posts")
		return result.fetchall()


	def get_AllBuyOnly_username(self):
		result = self.cursor.execute("SELECT username FROM posts")
		return result.fetchall()

	def get_AllBuyOnly_city(self):
		result = self.cursor.execute("SELECT city FROM posts")
		return result.fetchall()

	def get_AllBuyOnly_description(self):
		result = self.cursor.execute("SELECT description FROM posts")
		return result.fetchall()

	def get_AllUsers(self):
		result = self.cursor.execute("SELECT user_id FROM posts")
		return result.fetchall()





	def get_AllBuyOnly_by_model(self, model):
		result = self.cursor.execute("SELECT model FROM posts WHERE model = ?",(model,))
		return result.fetchall()

	def get_AllBuyOnly_price_by_model(self, model):
		result = self.cursor.execute("SELECT whats_trade FROM posts WHERE model = ?",(model,))
		return result.fetchall()


	def get_AllBuyOnly_username_by_model(self, model):
		result = self.cursor.execute("SELECT username FROM posts WHERE model = ?",(model,))
		return result.fetchall()

	def get_AllBuyOnly_city_by_model(self, model):
		result = self.cursor.execute("SELECT city FROM posts WHERE model = ?",(model,))
		return result.fetchall()

	def get_AllBuyOnly_description_by_model(self, model):
		result = self.cursor.execute("SELECT description FROM posts WHERE model = ?",(model,))
		return result.fetchall()

	def get_AllUsers_by_model(self, model):
		result = self.cursor.execute("SELECT user_id FROM posts WHERE model = ?",(model,))
		return result.fetchall()

	def get_Allid(self):
		result = self.cursor.execute("SELECT id FROM posts")
		return result.fetchall()

	def get_Allmodel(self):
		result = self.cursor.execute("SELECT model FROM posts")
		return result.fetchall()

