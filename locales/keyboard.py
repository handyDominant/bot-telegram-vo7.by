from pyrogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, Message, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InputMediaPhoto


class Button:
	def __init__(self, text: str, command: None):
		self.text = text
		self.command = command

	
	def create_url(self):
		return InlineKeyboardButton(self.text, url=self.command)
	def create(self):
		return InlineKeyboardButton(self.text, self.command)