import datetime
import os
import random
import string
import pyrogram
from db import BotDB
from config import db_path
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, Message, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InputMediaPhoto
from asyncio import sleep
import asyncio
import re
from loader import app
import logging
from logging import log
from pyrogram.errors import BotGroupsBlocked, ChatInvalid, FloodWait, UserDeactivated, MessageDeleteForbidden
import json
import requests
from pyrogram.types import ChatPermissions
from locales.keyboard import Button

BotDB = BotDB(db_path)
helps = f"🧑‍💻**Техническая помощь, возражения и предложения:**\n📞**Связь:**  @vo7_admin\n🏠**Домой:**  /start"

#sell_data
sell_photo = {}
sell_model = {}
sell_budjet = {}
sell_city = {}
sell_description = {}
sell_contact = {}

#buy_data
buy_photo = {}
buy_model = {}
buy_budjet = {}
buy_city = {}
buy_description = {}
buy_contact = {}

#user_data
photo = {}
model = {}
budjet = {}
photo = {}
city = {}
desc = {}
contact = {}
description = {}
group_photos = []

# Configure logging
logging.basicConfig(level=logging.INFO)

# logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


BotDB.CreateTableUsers()
BotDB.CreateTablePosts()













# --------- locales ----------
def generate_photoname(length=15):
	letters = string.ascii_lowercase
	rand_string = ''.join(random.choice(letters) for i in range(length))
	return rand_string

def get_users():
	"""
	Return users list

	In this example returns some random ID's
	"""
	yield from (451658425, 608551286, 78378343, 98765431, 12345678)


async def send_messages(user_id: int, text: str, disable_notification: bool = False) -> bool:
	"""
	Safe messages sender

	:param user_id:
	:param text:
	:param disable_notification:
	:return:
	"""
	try:
		await app.send_message(user_id, text, disable_notification=disable_notification)
	except BotGroupsBlocked:
		log.error(f"Target [ID:{user_id}]: blocked by user")
	except ChatInvalid:
		log.error(f"Target [ID:{user_id}]: invalid user ID")
	except FloodWait as e:
		log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
		await asyncio.sleep(e.timeout)
		return await send_messages(user_id, text)  # Recursive call
	except UserDeactivated:
		log.error(f"Target [ID:{user_id}]: user is deactivated")
	else:
		log.info(f"Target [ID:{user_id}]: success")
		return True
	return False

async def broadcaster() -> int:
	"""
	Simple broadcaster

	:return: Count of messages
	"""
	count = 0
	try:
		for user_id in get_users():
			if await send_messages(user_id, '<b>Hello!</b>'):
				count += 1
			await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
	finally:
		log.info(f"{count} messages successful sent.")

	return count


def DeleteExtraInfo(user_id):
	"""deleting extra users where id is user_id"""
	with open('locales/message_urls') as f:
		lines = f.readlines()
	pattern = re.compile(re.escape(str(user_id)))
	with open('locales/message_urls', 'w') as f:
		for line in lines:
			result = pattern.search(line)
			if result is None:
				f.write(line) 
				
def data():
	parse_date = str(datetime.datetime.now().date()).replace("datetime.date", "").replace("(", "").replace(")", "")
	parse_time = str(datetime.datetime.now().time()).split(".")
	parse_time = parse_time[0]
	return [parse_time, parse_date]



# ----------- Commands ----------- #
@app.on_message(filters.command('start', prefixes='/') & filters.private)
async def on_Start(_, c):
	"""On 'start' mess handler"""
	photo_counter[c.from_user.id] = 0
	sell_photo[c.from_user.id] = 0
	sell_model[c.from_user.id] = 0
	sell_budjet[c.from_user.id] = 0
	sell_city[c.from_user.id] = 0
	sell_description[c.from_user.id] = 0
	sell_contact[c.from_user.id] = 0

	#buy_data
	buy_photo[c.from_user.id] = 0
	buy_model[c.from_user.id] = 0
	buy_budjet[c.from_user.id] = 0
	buy_city[c.from_user.id] = 0
	buy_description[c.from_user.id] = 0
	buy_contact[c.from_user.id] = 0
	reg_date = data()
	reg_date = reg_date[0] + " " + reg_date[1]
	
	# код для поиска сообщения по ид
	with open("locales/message_urls") as openfile:
		for line in openfile:
			if f'{c.from_user.id}' in line:
				txt_message_id = int(line.replace('\n', '').replace(" ", "").split(",")[1])
				try:
					await app.delete_messages(c.from_user.id, txt_message_id)
				except MessageDeleteForbidden:
					pass
	openfile.close()
	DeleteExtraInfo(c.from_user.id)
	if c.from_user is not None:
		message_id = c.id
		username = c.from_user.username
		is_bot = 0
		language_code = 0
		chat_id = c.chat.id
		user_id = c.from_user.id
		first_name = c.from_user.first_name
		texts = c.text
		type1 = "private"
		bot_message_language = 0
		balance = 0
		orders = 0
		role = None

		# add users
		day_limit = 50

		inf_list = (user_id, chat_id, bot_message_language, language_code, message_id, is_bot,
					first_name, username, role, texts, type1, balance, reg_date, orders)

		BotDB.AddUser(inf_list) #method AddUser for add user to data base
		txt_export = open("locales/message_urls", 'a+')
		user_id = c.chat.id
		# записываем сообщение с коммандой старт
		txt_export.write(
			f"{str(c.chat.id)}, {str(c.id)}\n")  # записываем id в текстовый файл, all users
		start_message = f"✌🏻**Привет, {c.from_user.first_name}!\n🍎Я бот-барахолки!**\n**Я могу осуществлять авто-публикацию**\n📊Быстрое меню"
		await app.send_message(chat_id, start_message, 
		reply_markup=InlineKeyboardMarkup([[
		InlineKeyboardButton("💸Купить", callback_data=f"buy"), 
		InlineKeyboardButton("🤝Продать", callback_data=f"sell"), 
		InlineKeyboardButton("🛠Запчасти", url=f"t.me/gsm_zapchasti")], 
		[InlineKeyboardButton("🏥Сервисные центры", callback_data=f"service_centre"),
		 InlineKeyboardButton("❤️‍🔥Донат / Оплата", callback_data=f"donate_or_pay")], 
		[InlineKeyboardButton("📰Новости", url=f"t.me/apple_news_belarus"),
		 InlineKeyboardButton("🌐О нас", callback_data=f"by_as")], 
		[InlineKeyboardButton("⁉️Помощь|Регламент", callback_data=f"help")]]))

@app.on_message(filters.command('help', prefixes='/') & filters.private)
async def on_Help(_, c):
	await c.reply(helps)













@app.on_callback_query(filters.create(lambda _, __, c: c.data == "sell"))
async def sellButton(_, c):
	photo_counter[c.from_user.id] = 0
	sell_photo[c.from_user.id] = 0
	sell_model[c.from_user.id] = 0
	sell_budjet[c.from_user.id] = 0
	sell_city[c.from_user.id] = 0
	sell_description[c.from_user.id] = 0
	sell_contact[c.from_user.id] = 0

	#buy_data
	buy_photo[c.from_user.id] = 0
	buy_model[c.from_user.id] = 0
	buy_budjet[c.from_user.id] = 0
	buy_city[c.from_user.id] = 0
	buy_description[c.from_user.id] = 0
	buy_contact[c.from_user.id] = 0
	await c.edit_message_text("💸Какая техника\nвас интересует?", reply_markup=InlineKeyboardMarkup([[
		InlineKeyboardButton("🆕Новая", url=f"t.me/vo7_admin"), InlineKeyboardButton("🆗Б|У", f"sell_was/used")],
		[InlineKeyboardButton("⏮ Назад", f"menu")]]))

@app.on_callback_query(filters.create(lambda _, __, c: c.data == "sell_was/used"))
async def sell_wasusedButton(_, c):
	if c.from_user.id in photo:
		await c.edit_message_text(f"📸Вы уже оставили фотографию\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_model_w/u")], [InlineKeyboardButton("📊переотправить", f'new_sellphoto')]]))
		
	else:
		sell_photo[c.from_user.id] = 1
		await c.edit_message_text("📸Отправьте фотографию\nВашего устройства\n```отправьте фото в ответ на это сообщение!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", f"sell")]]))


photo_counter = {}

@app.on_message(filters.create(lambda _, __, c: sell_photo[c.from_user.id] == 1) & filters.private)
async def get_photo(_, c):
	photo_counter[c.from_user.id] += 1
	count = photo_counter[c.from_user.id]
	
	if c.text is not None:
		await c.reply("😥__Кажись вы отправили текст.\nОтправьте фото__")

	else:
		photo[c.from_user.id] = generate_photoname()
		group_photos.append(f"{c.from_user.id} {photo[c.from_user.id]}")
		await app.download_media(c.photo, f"data/sell/{c.from_user.id} {photo[c.from_user.id]}.png")
		if count == 1:
			await app.send_message(c.chat.id, f"📸Вы уже оставили фотографию\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_model_w/u")], [InlineKeyboardButton("📊переотправить", f'new_sellphoto')]]))
		sell_photo[c.from_user.id] = 0
		photo_counter[c.from_user.id] = 0




@app.on_message(filters.create(lambda _, __, c: sell_model[c.from_user.id] == 1) & filters.private)
async def get_model(_, c):
	if len(c.text) < 3:
			await app.send_message(c.chat.id, "😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f'sell_model_w/u')]]))
	else:
		model[c.from_user.id] = c.text
		sell_model[c.from_user.id] = 0
		await app.send_message(c.chat.id, f"📱Модель: {c.text}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_budjet_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellmodel')]]))





@app.on_callback_query(filters.create(lambda _, __, c: "sell_budjet_w/u" == c.data))
async def sell_budjetwasusedButton(_, c):
	
	if c.from_user.id in budjet:
		await c.edit_message_text(f"💰Цена до: {budjet[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_contact_inform_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellbudjet')]]))
	else:
		sell_budjet[c.from_user.id] = 1
		await c.edit_message_text("💰Введите стоимость\nвашего устройства\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "sell_model_w/u")]]))





@app.on_callback_query(filters.create(lambda _, __, c: c.data == "sell_model_w/u"))
async def sell_model_wasusedButton(_, c):
	if c.from_user.id in model:
		await c.edit_message_text(f"📱Модель: {model[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_budjet_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellmodel')]]))
		
	else:
		sell_model[c.from_user.id] = 1
		await c.edit_message_text("📱Укажите модель устройства\nкоторую Вы желаете приобрести\n__(пример: Apple iPhone 11 64gb Black):__\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", f"sell_was/used")]]))


@app.on_message(filters.create(lambda _, __, c: sell_budjet[c.from_user.id] == 1) & filters.private)
async def get_model(_, c):
	if len(c.text) < 2:
		await c.reply("😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f'sell_model_w/u')]]))
	else:
		sell_budjet[c.from_user.id] = 0
		budjet[c.from_user.id] = c.text
		await c.reply(f"💰Цена до: {budjet[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_contact_inform_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellbudjet')]]))

@app.on_message(filters.create(lambda _, __, c: sell_description[c.from_user.id] == 1) & filters.private)
async def get_budjet(_, c):
	if len(c.text) < 2:
		await app.send_message(c.chat.id,"😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f"sell_description_w/u")]]))

	else:
		description[c.from_user.id] = c.text
		sell_description[c.from_user.id] = 0
		await app.send_message(c.chat.id, f"📃Вы ввели описание:\n{description[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_post_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_selldescription')]]))



@app.on_message(filters.create(lambda _, __, c: sell_contact[c.from_user.id] == 1) & filters.private)
async def get_contacts(_, c):
	if len(c.text) < 2:
		await app.send_message(c.chat.id, "😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f"sell_budjet_w/u")]]))

	else:
		sell_contact[c.from_user.id] = 0
		contact[c.from_user.id] = c.text
		await app.send_message(c.chat.id, f"📞Контактная информация: {c.text}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_city_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_contact')]]))


@app.on_message(filters.create(lambda _, __, c: sell_city[c.from_user.id] == 1) & filters.private)
async def get_city(_, c):
	if len(c.text) < 2:
		await app.send_message(c.chat.id,  "😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f"sell_city_w/u")]]))

	else:
		city[c.from_user.id] = c.text
		sell_city[c.from_user.id] = 0
		await app.send_message(c.chat.id, f"🏙город/страна: {c.text}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_description_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellcity')]]))












@app.on_callback_query(filters.create(lambda _, __, c: "sell_contact_inform_w/u" in c.data))
async def sell_contactwasusedButton(_, c):
	if c.from_user.id in contact:
		await c.edit_message_text(f"📞Контактная информация: {contact[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_city_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellcontact')]]))
	else:
		sell_contact[c.from_user.id] = 1
		await c.edit_message_text("📞Введите контактную информацию\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "sell_budjet_w/u")]]))





@app.on_callback_query(filters.create(lambda _, __, c: "sell_city_w/u" in c.data))
async def sell_citywasusedButton(_, c):
	if c.from_user.id in city:
		await c.edit_message_text(f"🏙город/страна: {city[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_description_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_sellcity')]]))
	else:
		sell_city[c.from_user.id] = 1
		await c.edit_message_text("🏙Введите город/страну\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "sell_contact_inform_w/u")]]))

@app.on_callback_query(filters.create(lambda _, __, c: "sell_description_w/u" == c.data))
async def sell_descriptionwasusedButton(_, c):
	if c.from_user.id in description:
		await c.edit_message_text(f"📃Вы ввели описание:\n{description[c.from_user.id]}\n__нажмите **Далее** если верно__",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"sell_post_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_selldescription')]]))
	else:
		sell_description[c.from_user.id] = 1
		await c.edit_message_text("📃Опишите состояние, причину и условия продажи вышего устройства:\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "sell_city_w/u")]]))










@app.on_callback_query(filters.create(lambda _, __, c: "sell_post_w/u" == c.data))
async def postwasusedButton(_, c):
	s_photo = photo[c.from_user.id]
	name = c.from_user.mention()
	device = model[c.from_user.id]
	whats_trade = budjet[c.from_user.id]
	desc = description[c.from_user.id]
	place = city[c.from_user.id]
	
	text = f"""
	💼Пост о продаже:

	```{device}```

	__{desc}__

	💰Стоимость: ```{whats_trade}```

	{place}

	☎Контакты/тг: {contact[c.from_user.id]}
				"""
	await c.edit_message_text(text + "\n\nДействительно опубликовать?\n❗**Вы можете продать технику в течении часа до 80% от рыночной стоимости!**\n__для этого нажмите __**⚠Быстро**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤Отправить", f"send_to_chat_sell")], [InlineKeyboardButton("⚠Быстро", f"send_to_chat_fast")], [InlineKeyboardButton("🔁Исправить", f"edit_sell_post")]]))


@app.on_callback_query(filters.create(lambda _, __, c: "edit_sell_post" == c.data))
async def edit_buy_postButton(_, c):
	await c.edit_message_text("🔁Что хотите исправить?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📸фото", "sell_was/used")], [InlineKeyboardButton("📱модель", "sell_model_w/u")], [InlineKeyboardButton("💰бюджет", "sell_budjet_w/u")], [InlineKeyboardButton("☎контакты", "sell_contact_inform_w/u")], [InlineKeyboardButton("🌆страну/город", "sell_city_w/u")], [InlineKeyboardButton("📃описание", "sell_description_w/u")], [InlineKeyboardButton("вернуться", "sell_post_w/u")]]))


@app.on_callback_query(filters.create(lambda _, __, c: "send_to_chat_sell" == c.data))
async def sendtochatBuyPostButton(_, c):
	s_photo = photo[c.from_user.id]
	desc = description[c.from_user.id]
	user_id = c.from_user.id
	name = c.from_user.first_name
	device = model[c.from_user.id]
	whats_trade = budjet[c.from_user.id]
	place = city[c.from_user.id]
	reg_date = data()
	reg_date = reg_date[0] + " " + reg_date[1]
	text = f"""
	💼Пост о продаже:

	```{device}```

	__{desc}__

	💰Стоимость: ```{whats_trade}```

	{place}
	☎Контакты/тг: {contact[c.from_user.id]}
				"""
	inf_list = (user_id, c.id, text, device, name, place, desc, reg_date,
						whats_trade)
	BotDB.AddPost(inf_list)
	await c.edit_message_text("✅заявка отправлена в группу @apple_belarus", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊меню", f"menu")]]))
	board = []
	i = 0
	for inputs in group_photos:
		if f"{c.from_user.id}" in inputs:
			i += 1
			if i == 1:
				board.append(InputMediaPhoto("data/sell/" + inputs + ".png", caption=text + "\n\n🤖Опубликовать объявление: @vo7_bot"))
			else:
				board.append(InputMediaPhoto("data/sell/" + inputs + ".png"))

		

	await app.send_media_group('apple_belarus', board)
	
	model.pop(c.from_user.id)
	budjet.pop(c.from_user.id)
	contact.pop(c.from_user.id)
	city.pop(c.from_user.id)
	description.pop(c.from_user.id)
	for i in group_photos:
		if f"{c.from_user.id}" in i:
			os.remove("data/sell/" + i + ".png")
			group_photos.remove(i)
	photo.pop(c.from_user.id)




@app.on_callback_query(filters.create(lambda _, __, c: "send_to_chat_fast" == c.data))
async def sendtochatfastPostButton(_, c):
	s_photo = photo[c.from_user.id]
	desc = description[c.from_user.id]
	user_id = c.from_user.id
	name = c.from_user.first_name
	device = model[c.from_user.id]
	whats_trade = budjet[c.from_user.id]
	place = city[c.from_user.id]
	reg_date = data()
	reg_date = reg_date[0] + " " + reg_date[1]
	text = f"""
	⚠Быстрая заявка
	💼Пост о продаже:

	```{device}```

	__{desc}__

	💰Стоимость: ```{whats_trade}```

	{place}
	☎Контакты/тг: {contact[c.from_user.id]}

				"""
	inf_list = (user_id, c.id, text, device, name, place, desc, reg_date,
						whats_trade)
	BotDB.AddPost(inf_list)
	await c.edit_message_text("✅Спасибо! Ближайший освободившийся менеджер свяжется с Вами!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊меню", f"menu")]]))
	board = []
	i = 0
	for inputs in group_photos:
		if f"{c.from_user.id}" in inputs:
			i += 1
			if i == 1:
				board.append(InputMediaPhoto("data/sell/" + inputs + ".png", caption=text + "\n\n🤖Опубликовать объявление: @vo7_bot"))
			else:
				board.append(InputMediaPhoto("data/sell/" + inputs + ".png"))
	
	await app.send_media_group('vo7_admin', board)

	model.pop(c.from_user.id)
	budjet.pop(c.from_user.id)
	contact.pop(c.from_user.id)
	city.pop(c.from_user.id)
	description.pop(c.from_user.id)
	for i in group_photos:
		if f"{c.from_user.id}" in i:
			os.remove("data/sell/" + i + ".png")
			group_photos.remove(i)
	photo.pop(c.from_user.id)







@app.on_callback_query(filters.create(lambda _, __, c: c.data == "buy"))
async def buyButton(_, c):
	photo_counter[c.from_user.id] = 0
	sell_photo[c.from_user.id] = 0
	sell_model[c.from_user.id] = 0
	sell_budjet[c.from_user.id] = 0
	sell_city[c.from_user.id] = 0
	sell_description[c.from_user.id] = 0
	sell_contact[c.from_user.id] = 0

	#buy_data
	buy_photo[c.from_user.id] = 0
	buy_model[c.from_user.id] = 0
	buy_budjet[c.from_user.id] = 0
	buy_city[c.from_user.id] = 0
	buy_description[c.from_user.id] = 0
	buy_contact[c.from_user.id] = 0
	await c.edit_message_text("💸Какая техника\nвас интересует?", reply_markup=InlineKeyboardMarkup([[
		InlineKeyboardButton("🆕Новая", url=f"t.me/vo7_admin"), InlineKeyboardButton("🆗Б|У", f"was/used")],
		[InlineKeyboardButton("⏮ Назад", f"menu")]]))

@app.on_callback_query(filters.create(lambda _, __, c: c.data == "menu"))
async def menuButton(_, c):
	photo_counter[c.from_user.id] = 0
	sell_photo[c.from_user.id] = 0
	sell_model[c.from_user.id] = 0
	sell_budjet[c.from_user.id] = 0
	sell_city[c.from_user.id] = 0
	sell_description[c.from_user.id] = 0
	sell_contact[c.from_user.id] = 0

	#buy_data
	buy_photo[c.from_user.id] = 0
	buy_model[c.from_user.id] = 0
	buy_budjet[c.from_user.id] = 0
	buy_city[c.from_user.id] = 0
	buy_description[c.from_user.id] = 0
	buy_contact[c.from_user.id] = 0
	start_message = f"📊Быстрое меню"
	await c.edit_message_text(
		start_message,
		reply_markup=InlineKeyboardMarkup([[
		InlineKeyboardButton("💸Купить", callback_data=f"buy"), 
		InlineKeyboardButton("🤝Продать", callback_data=f"sell"), 
		InlineKeyboardButton("🛠Запчасти", url=f"t.me/gsm_zapchasti")], 
		[InlineKeyboardButton("🏥Сервисные центры", callback_data=f"service_centre"),
		 InlineKeyboardButton("❤️‍🔥Донат / Оплата", url=f"t.me/vo7_admin")], 
		[InlineKeyboardButton("📰Новости", url=f"t.me/apple_news_belarus"),
		 InlineKeyboardButton("🌐О нас", callback_data=f"by_as")], 
		[InlineKeyboardButton("⁉️Помощь|Регламент", callback_data=f"help")]]))


@app.on_callback_query(filters.create(lambda _, __, c: c.data == "service_centre"))
async def service_centreButton(_, c):
	await c.edit_message_text("💼Хотите заключить партнерку?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊Заключить", url="t.me/vo7_admin")], [InlineKeyboardButton("⏮ Назад", f"menu")]]))



@app.on_callback_query(filters.create(lambda _, __, c: c.data == "help"))
async def helpButton(_, c):
	await c.edit_message_text(f"⁉️Помощь|Регламент", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❗️Администрация", url="t.me/vo7_admin"),InlineKeyboardButton("❓Регламент", url="https://clck.ru/S7CAn")], [InlineKeyboardButton("⏮ Назад", f"menu")]]))



@app.on_callback_query(filters.create(lambda _, __, c: c.data == "by_as"))
async def by_asButton(_, c):
	await c.edit_message_text(f"🌐О нас:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥Группы", "groups"),InlineKeyboardButton("💻Сайт", url="vo7.by")],[InlineKeyboardButton("VK", url="vk.com/vo7by"), InlineKeyboardButton("Instagram", url="instagram.com/apple_belarus_minsk")],  [InlineKeyboardButton("⏮ Назад", f"menu")]]))




@app.on_callback_query(filters.create(lambda _, __, c: c.data == "groups"))
async def groupsButton(_, c):
	await c.edit_message_text("👥Группы", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📱Samsung", url="t.me/samsung_belarus")], 
	[InlineKeyboardButton("📱Xiaomi", url="t.me/mi_belarus")],
	[InlineKeyboardButton("🍎Apple", url="t.me/apple_belarus")],
	[InlineKeyboardButton("⏮ Назад", "by_as")]]))










@app.on_callback_query(filters.create(lambda _, __, c: c.data == "was/used"))
async def wasusedButton(_, c):
	if c.from_user.id in model:
		await c.edit_message_text(f"📱Модель: {model[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"budjet_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_model')]]))
		
	else:
		buy_model[c.from_user.id] = 1
		await c.edit_message_text("📱Укажите модель устройства\nкоторую Вы желаете приобрести\n__(пример: Apple iPhone 11 64gb Black):__\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", f"buy")]]))





@app.on_callback_query(filters.create(lambda _, __, c: "budjet_w/u" in c.data))
async def budjetwasusedButton(_, c):
	
	if c.from_user.id in budjet:
		await c.edit_message_text(f"💰Бюджет до: {budjet[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"contact_inform_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_budjet')]]))
	else:
		buy_budjet[c.from_user.id] = 1
		await c.edit_message_text("💰Введите бюджет на\nкоторый вы рассчитываете\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "was/used")]]))


@app.on_callback_query(filters.create(lambda _, __, c: "new_" in c.data))
async def newwasusedButton(_, c):
	new = c.data.split("new_")[1]
	match new:
		case "model":
			model.pop(c.from_user.id)
			await wasusedButton(_, c)
		case "budjet":
			budjet.pop(c.from_user.id)
			await budjetwasusedButton(_, c)
		case "contact":
			contact.pop(c.from_user.id)
			await contactwasusedButton(_, c)
		case "city":
			city.pop(c.from_user.id)
			await citywasusedButton(_, c)
		case "sellphoto":
			for i in group_photos:
				if f"{c.from_user.id}" in i:
					os.remove("data/sell/" + i + ".png")
					group_photos.remove(i)
			photo.pop(c.from_user.id)
			
			await sell_wasusedButton(_, c)
		case "sellmodel":
			model.pop(c.from_user.id)
			await sell_model_wasusedButton(_, c)
		case "sellbudjet":
			budjet.pop(c.from_user.id)
			await sell_budjetwasusedButton(_, c)
		case "sellcontact":
			contact.pop(c.from_user.id)
			await sell_contactwasusedButton(_, c)
		case "sellcity":
			description.pop(c.from_user.id)
			await sell_descriptionwasusedButton(_, c)

		case "selldescription":
			city.pop(c.from_user.id)
			await sell_citywasusedButton(_, c)	

@app.on_callback_query(filters.create(lambda _, __, c: "contact_inform_w/u" in c.data))
async def contactwasusedButton(_, c):
	if c.from_user.id in contact:
		await c.edit_message_text(f"☎Контактная информация: {contact[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"city_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_contact')]]))
	else:
		buy_contact[c.from_user.id] = 1
		await c.edit_message_text("☎Введите контактную информацию\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "budjet_w/u")]]))


@app.on_callback_query(filters.create(lambda _, __, c: "city_w/u" in c.data))
async def citywasusedButton(_, c):
	if c.from_user.id in city:
		await c.edit_message_text(f"🌆город/страна: {city[c.from_user.id]}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"post_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_city')]]))
	else:
		buy_city[c.from_user.id] = 1
		await c.edit_message_text("🌆Введите город/страну\n\n```оправьте сообщение в ответ на это!```", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚫Отмена", "contact_inform_w/u")]]))

@app.on_callback_query(filters.create(lambda _, __, c: "post_w/u" == c.data))
async def postwasusedButton(_, c):
	name = c.from_user.mention()
	device = model[c.from_user.id]
	whats_trade = budjet[c.from_user.id]
	place = city[c.from_user.id]
	
	text = f"""
	💼Пост о покупке:

	```{device}```
	
	💰**Цена до:** {whats_trade}

	{place}
	☎**Контакты/тг: {contact[c.from_user.id]}
				"""
	await c.edit_message_text(text + "\n\nДействительно опубликовать?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤Отправить", f"send_to_chat_buy")], [InlineKeyboardButton("🔁Исправить", f"edit_buy_post")]]))



@app.on_callback_query(filters.create(lambda _, __, c: "edit_buy_post" == c.data))
async def edit_buy_postButton(_, c):
	await c.edit_message_text("🔁Что хотите исправить?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📱модель", "was/used")], [InlineKeyboardButton("💰бюджет", "budjet_w/u")], [InlineKeyboardButton("☎контакты", "contact_inform_w/u")], [InlineKeyboardButton("🌆страну/город", "city_w/u")], [InlineKeyboardButton("вернуться", "post_w/u")]]))





@app.on_message(filters.create(lambda _, __, c: buy_model[c.from_user.id] == 1)& filters.private)
async def get_model(_, c):
	if len(c.text) < 3:
			await app.send_message(c.chat.id, "😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f'was/used')]]))
	else:
		model[c.from_user.id] = c.text
		buy_model[c.from_user.id] = 0
		await app.send_message(c.chat.id, f"📱Модель: {c.text}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"budjet_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_model')]]))

@app.on_message(filters.create(lambda _, __, c: buy_budjet[c.from_user.id] == 1)& filters.private)
async def get_model(_, c):
	if len(c.text) < 2:
		await c.reply("😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f'was/used')]]))
	else:
		buy_budjet[c.from_user.id] = 0
		budjet[c.from_user.id] = c.text
		await c.reply(f"💰Цена до: {budjet[c.from_user.id]}\n__нажмите **Далее** если верно__",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"contact_inform_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_budjet')]]))


@app.on_message(filters.create(lambda _, __, c: buy_contact[c.from_user.id] == 1)& filters.private)
async def get_contacts(_, c):
	if len(c.text) < 2:
		await app.send_message(c.chat.id, "😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f"budjet_w/u")]]))

	else:
		buy_contact[c.from_user.id] = 0
		contact[c.from_user.id] = c.text
		await app.send_message(c.chat.id, f"📞Контактная информация: {c.text}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"city_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_contact')]]))


@app.on_message(filters.create(lambda _, __, c: buy_city[c.from_user.id] == 1)& filters.private)
async def get_city(_, c):
	if len(c.text) < 2:
		await app.send_message(c.chat.id,  "😥__Слишком короткий текст.\nПопробуйте еще раз:__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍎Вернуться", f"city_w/u")]]))

	else:
		city[c.from_user.id] = c.text
		buy_city[c.from_user.id] = 0
		await app.send_message(c.chat.id, f"🏙город/страна: {c.text}\n__нажмите **Далее** если верно__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Далее", f"post_w/u")], [InlineKeyboardButton("📊перезаписать", f'new_city')]]))





@app.on_callback_query(filters.create(lambda _, __, c: "send_to_chat_buy" in c.data))
async def sendtochatBuyPostButton(_, c):
	user_id = c.from_user.id
	name = c.from_user.first_name
	device = model[c.from_user.id]
	whats_trade = budjet[c.from_user.id]
	place = city[c.from_user.id]
	reg_date = data()
	reg_date = reg_date[0] + " " + reg_date[1]
	text = f"""
	💼Пост о покупке:

	```{device}```

	__{desc}__

	💰Цена до: ```{whats_trade}```

	{place}
	☎Контакты/тг: {contact[c.from_user.id]}
				"""
	inf_list = (user_id, c.id, text, device, name, place, "покупка", reg_date,
						whats_trade)
	BotDB.AddPost(inf_list)
	await c.edit_message_text("✅заявка отправлена в группу @apple_belarus", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊меню", f"menu")]]))
	await app.send_message('apple_belarus', text + "\n\n🤖Опубликовать объявление: @vo7_bot")
	
	model.pop(c.from_user.id)
	budjet.pop(c.from_user.id)
	contact.pop(c.from_user.id)
	city.pop(c.from_user.id)





@app.on_message(filters.new_chat_members, group=1)
async def NewChatMember(_, c):
	await app.restrict_chat_member(c.chat.id, c.from_user.id, ChatPermissions())
	await app.send_message(c.chat.id, f"💻Здравствуйте, {c.from_user.mention()}!\nРады Вас приветствовать в группе @apple_belarus 🤓\n📃Настоятельно рекомендуем ознакомиться с ботом нашей группы @vo7_bot!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖воспользоваться ботом", url="https://t.me/vo7_bot")]]))

@app.on_callback_query(filters.create(lambda _, __, c: "from chat to ct" == c.data))
async def edit_sendcatalog(_, c):
	photo_counter[c.from_user.id] = 0
	sell_photo[c.from_user.id] = 0
	sell_model[c.from_user.id] = 0
	sell_budjet[c.from_user.id] = 0
	sell_city[c.from_user.id] = 0
	sell_description[c.from_user.id] = 0
	sell_contact[c.from_user.id] = 0

	#buy_data
	buy_photo[c.from_user.id] = 0
	buy_model[c.from_user.id] = 0
	buy_budjet[c.from_user.id] = 0
	buy_city[c.from_user.id] = 0
	buy_description[c.from_user.id] = 0
	buy_contact[c.from_user.id] = 0
	await c.answer("🤓Вам написал @vo7_bot\n🚀Проверьте личные сообщения!", True)
	await app.send_message(c.from_user.id, "**🚀Добро пожаловать в наш каталог**\n__Ищи клиента/продовца удобнее!__", reply_markup=InlineKeyboardMarkup([

		[InlineKeyboardButton("🔍поиск", callback_data=f"catalogs_0")]]))


#@app.on_callback_query(filters.create(lambda _, __, c: "catalog" == c.data))
#async def edit_catalog(_, c):
#	photo_counter[c.from_user.id] = 0
#	sell_photo[c.from_user.id] = 0
#	sell_model[c.from_user.id] = 0
#	sell_budjet[c.from_user.id] = 0
#	sell_city[c.from_user.id] = 0
#	sell_description[c.from_user.id] = 0
#	sell_contact[c.from_user.id] = 0
#
#	#buy_data
#	buy_photo[c.from_user.id] = 0
#	buy_model[c.from_user.id] = 0
#	buy_budjet[c.from_user.id] = 0
#	buy_city[c.from_user.id] = 0
#	buy_description[c.from_user.id] = 0
#	buy_contact[c.from_user.id] = 0
#	await c.edit_message_text("**🚀Добро пожаловать в наш каталог**\n__Ищи клиента/продовца удобнее!__", reply_markup=InlineKeyboardMarkup([
#
#		[InlineKeyboardButton("🔍поиск", callback_data=f"catalogs_0")]]))
#
#
#
#@app.on_message(filters.command('catalog', prefixes='*') & filters.private)
#async def on_Catalog(_, c):
#	photo_counter[c.from_user.id] = 0
#	sell_photo[c.from_user.id] = 0
#	sell_model[c.from_user.id] = 0
#	sell_budjet[c.from_user.id] = 0
#	sell_city[c.from_user.id] = 0
#	sell_description[c.from_user.id] = 0
#	sell_contact[c.from_user.id] = 0
#
#	#buy_data
#	buy_photo[c.from_user.id] = 0
#	buy_model[c.from_user.id] = 0
#	buy_budjet[c.from_user.id] = 0
#	buy_city[c.from_user.id] = 0
#	buy_description[c.from_user.id] = 0
#	buy_contact[c.from_user.id] = 0
#	count = len(BotDB.get_AllUsers())
#	print(count)
#	r_c = random.randint(1, count)
#	print(r_c)
#	await app.send_message(c.from_user.id, "**🚀Добро пожаловать в наш каталог**\n__Ищи клиента/продовца удобнее!__", reply_markup=InlineKeyboardMarkup([

	#	[InlineKeyboardButton("🔍поиск", callback_data=f"catalogs_{r_c}")], [InlineKeyboardButton("📄свой пост")]]))

def get_pagesmodel(i):
	model = BotDB.get_AllBuyOnly_model()[i]

	CONTENT = f"{model}"
	return str(CONTENT).strip("('',)")

def get_pagesprice(i):
	model = BotDB.get_AllBuyOnly_price()[i]
	CONTENT = f"{model}"

	return CONTENT.strip("('',)")
def get_pagescity(i):
	city = BotDB.get_AllBuyOnly_city()[i]
	CONTENT = f"{city}"

	return CONTENT.strip("('',)")
def get_pagesusername(i):
	city = BotDB.get_AllBuyOnly_username()[i]
	CONTENT = f"{city}"

	return CONTENT.strip("('',)")


def get_pagesid(idd):
	
	CONTENT = f"{idd}"

	return int(CONTENT.strip("('',)"))












#@app.on_callback_query(filters.create(lambda _, __, c: "catalogs_" in c.data))
#async def edit_catalogbuy(_, c):
#
#	row = int(c.data.split("catalogs_")[1])
#	find_model[c.from_user.id] = 0
#	model = get_pagesmodel(row)
#	price = get_pagesprice(row)
#	city = get_pagescity(row)
#	username = get_pagesusername(row)
#	content = f""" 
#	📱Модель: {model}
#	💰Цена: {price}
#	🌆Город: {city}
#	☎Юзернейм: @{username}
#	"""
#	count = len(BotDB.get_AllUsers())
#	print(count)
#	r_c = random.randint(1, count)
#	print(r_c)
#
#	await c.edit_message_text(content, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔍поиск", callback_data=f"catalogs_{r_c}")],[#InlineKeyboardButton("📄фильтр", callback_data=f"filter")], [InlineKeyboardButton("назад", f"catalog")]]))
#
#
#find_model = {}
#find_model_name = {}
#@app.on_callback_query(filters.create(lambda _, __, c: "filter" == c.data))
#async def edit_filter(_, c):
#	find_model[c.from_user.id] = 1
#	await c.edit_message_text("🚀напишите модель\nкоторую ищете\n\n**❗Старайтесь указывать\nточную модель**")
#
#USERS_FILTER = {}
#
#
#@app.on_message(filters.create(lambda _, __, c: find_model[c.from_user.id] == 1)& filters.private)
#async def get_findmodel(_, c):
#	count = 0
#	list_id = BotDB.get_Allid()
#	model_li = BotDB.get_Allmodel()
#	for i in model_li:
#		print(i)
#		if c.text in f'{i}':
#			count += 1
#	keyboard = []
#	if count == 0:
#		content = "❌по этому запросу\nничего не найдено"
#		button = Button('назад', f'catalog')
#		keyboard.append([button.create()])
#	else:
#		
#		new_list_id = []
#		counter = 0
#		for i in model_li:
#			counter += 1
#			if c.text in f'{i}':
#				
#				new_list_id.append(counter)
#
#		row = 0
#		USERS_FILTER[c.from_user.id] = new_list_id
#		find_model_name[c.from_user.id] = c.text
#		idd = get_pagesid(new_list_id[row])
#		model = get_pagesmodel(idd)
#		price = get_pagesprice(idd)
#		city = get_pagescity(idd)
#		username = get_pagesusername(idd)
#		count_users = len(USERS_FILTER[c.from_user.id])
#		content = f""" 
#		📱Модель: {model}
#		💰Цена: {price}
#		🌆Город: {city}
#		☎Юзернейм: @{username}
#
#		```{row + 1} из {count_users}```
#		
#		"""
#
#		button = Button('далее', f'filtercats_{row + 1}')
#		button2 = Button('назад', f'catalog')
#		keyboard.append([button.create()])
#		keyboard.append([button2.create()])
#		
#
#		r_c = random.randint(1, count)
#
#	
#	markup = InlineKeyboardMarkup(keyboard)
#	await app.send_message(c.from_user.id, content, reply_markup=markup)
#	find_model[c.from_user.id] = 0
#	print(USERS_FILTER[c.from_user.id])
#
#
#

#@app.on_callback_query(filters.create(lambda _, __, c: "filtercats_" in c.data))
#async def edit_catalogbuy(_, c):
#	count = len(BotDB.get_AllUsers_by_model(find_model_name[c.from_user.id]))
#	keyboard = []
#	row = int(c.data.split("filtercats_")[1])
#	if row + 1 < 1:
#		await c.answer("❌дальше ничего нет")
#	else:
#
#		list_id = BotDB.get_Allid()
#		model_li = BotDB.get_Allmodel()
#		try:
#			idd = get_pagesid(USERS_FILTER[c.from_user.id][row])
#		
#		except IndexError as e:
#			await c.answer("❌дальше ничего нет")
#		
#		model = get_pagesmodel(idd)
#		price = get_pagesprice(idd)
#		city = get_pagescity(idd)
#		username = get_pagesusername(idd)
#		count_users = len(USERS_FILTER[c.from_user.id])
#		content = f""" 
#		📱Модель: {model}
#		💰Цена: {price}
#		🌆Город: {city}
#		☎Юзернейм: @{username}
#
#
#		```{row + 1} из {count_users}```
#		
#		"""
#
#
#		
#		try:
#			button = Button('>>>', f'filtercats_{row + 1}')
#			button2 = Button('<<<', f'filtercats_{row - 1}')
#
#		except Exception as e:
#			await c.answer("❌дальше ничего нет")
#
#		keyboard.append([button2.create(), button.create()])
#		keyboard.append([Button('назад', f'catalog').create()])
#		markup = InlineKeyboardMarkup(keyboard)
#		try:
#			await c.edit_message_text(content, reply_markup=markup)
#		
#		except pyrogram.errors.exceptions.bad_request_400.MessageNotModified as e:
#			await c.answer("❌дальше ничего нет")








app.run()