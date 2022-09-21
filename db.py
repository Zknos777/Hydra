import sqlite3

path = "database.db"

def create_db():
	connection = sqlite3.connect(path, check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER UNIQUE NOT NULL,active INTEGER DEFAULT(1))")
	connection.commit()

class DataBase:
	def __init__(self):
		self.connection = sqlite3.connect(path,check_same_thread=False)
		self.cursor = self.connection.cursor()
		
	def user_exists(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?",(user_id,)).fetchmany(1)
			return bool(len(result))
			
	def add_user(self, user_id):
		with self.connection:
			return self.cursor.execute('INSERT INTO `users` (`user_id`) VALUES (?)', (user_id,))
			
	def set_active(self, user_id, active):
		with self.connection:
			return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))
			
	def get_all_users(self):
		with self.connection:
			return self.cursor.execute("SELECT COUNT(*) FROM `users` WHERE `active` = 1").fetchall()
			
	def get_no_active_users(self):
		with self.connection:
			return self.cursor.execute("SELECT COUNT(*) FROM `users` WHERE `active` = 0").fetchall()
			
	def get_users(self):
		with self.connection:
			return self.cursor.execute("SELECT `user_id`,`active` FROM `users`").fetchall()

db = DataBase()