import sqlite3
import os.path

class Konexioa:
	__instance = None
	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(Konexioa, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance

	def __init__(self):
		if not self.__initialized:
			db_path = os.path.join(os.path.dirname(__file__), "..", "src", "datubase.db")
			self.con = sqlite3.connect("db_path", check_same_thread=False)
			self.cur = self.con.cursor()
			self.__initialized = True

	def select(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		rows = self.cur.fetchall()
		return [x for x in rows]

	def insert(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		self.con.commit()
		answ = self.cur.rowcount
		return answ

	def update(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		self.con.commit()

	def delete(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		answ = self.cur.rowcount
		self.con.commit()
		return answ