import os

import telebot
import requests
from telebot import types
base_url = os.getenv("TEAZONE_API_URL", "http://127.0.0.1:8000/api")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
if not bot_token:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")
bot = telebot.TeleBot(bot_token)


markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
markup.add(types.KeyboardButton("Buyurtma berish"), types.KeyboardButton('Dastavka'), types.KeyboardButton('Biz haqimizda'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	try:
		text = requests.get(f'{base_url}/info/').json()
		bot.send_message(message.from_user.id, text['text'], reply_markup=markup)
	except Exception as err:
		print(err)
		bot.reply_to(message, "hush kelibsiz!", reply_markup=markup)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	if message.text == "Biz haqimizda":
		query = requests.get(f'{base_url}/detail/').json()
		text = f"Tea-House choyhonasi\n{query['text']}\nTelefon nomer: {query['phone']}"
		bot.send_location(message.from_user.id, latitude=query['lat'], longitude=query['lng'], reply_markup=markup)
		bot.send_message(message.from_user.id, text)
	elif message.text == "Buyurtma berish":
		bot_message = bot.send_message(message.from_user.id, 'Ismingizni kiriting!',
									   reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(bot_message, phone_controller)
	elif message.text == "Dastavka":
		bot_message = bot.send_message(message.from_user.id, 'Ismingizni kiriting!',
									   reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(bot_message, dastavka_phone_controller)
	else:
		bot.reply_to(message, message.text)


def phone_controller(message):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		try:
			name = message.text
			contact_button = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
			contact_button.add(types.KeyboardButton("Raqam jo'natish", request_contact=True))
			bot_message = bot.send_message(message.from_user.id, 'Raqamingizni yuboring!', reply_markup=contact_button)
			bot.register_next_step_handler(bot_message, date_controller, name)
		except Exception as err:
			print(err)


def date_controller(message, name):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		if 'contact' in message.content_type:
			phone = message.contact.phone_number
			bot_message = bot.send_message(message.from_user.id, 'Sanani kiriting Masalan:(2022-12-18)!', reply_markup=types.ReplyKeyboardRemove())
			bot.register_next_step_handler(bot_message, room_controller, phone, name)
		else:
			bot.send_message(message.from_user.id, "Raqam notog'ri")
			send_welcome(message)


def dastavka_phone_controller(message):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		try:
			name = message.text
			contact_button = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
			contact_button.add(types.KeyboardButton("Raqam jo'natish", request_contact=True))
			bot_message = bot.send_message(message.from_user.id, 'Raqamingizni yuboring!', reply_markup=contact_button)
			bot.register_next_step_handler(bot_message, dastavka_date_controller, name)
		except Exception as err:
			print(err)


def dastavka_date_controller(message, name):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		if 'contact' in message.content_type:

			phone = message.contact.phone_number
			bot_message = bot.send_message(message.from_user.id, 'Sanani kiriting Masalan:(2022-12-18)!',
										   reply_markup=types.ReplyKeyboardRemove())

			bot.register_next_step_handler(bot_message, order_delivery_controller,phone, name)
		else:
			bot.send_message(message.from_user.id, 'Raqamingiz notogri')




def room_controller(message, phone, name):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		date = message.text
		qwer = {
			"date": date
		}
		query = requests.post(f'{base_url}/room/', data=qwer).json()
		room_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		buttons = []
		if query == []:
			bot.send_message(message.from_user.id,'Bu kunga afsuski bosh xona yoq',reply_markup=markup)

		else:
			for i in query:
				buttons.append(types.KeyboardButton(f"{i['number']}"))
				if len(buttons) == 2:
					room_markup.add(buttons[0], buttons[1])
					buttons.clear()
			if len(buttons) == 1:
				room_markup.add(buttons[0])
				buttons.clear()
			room_markup.add(types.KeyboardButton("Ortga"))
			bot_message = bot.send_message(message.from_user.id,'Hozirdagi bosh honalar Buyurtma berish uchun honani tanlang!', reply_markup=room_markup)
			bot.register_next_step_handler(bot_message, order_controller, date, phone, name)



def All_controller(message, phone, name):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		date = message.text
		query = requests.get(f'{base_url}/room/').json()
		all_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		buttons = []
		all_markup.add(types.KeyboardButton("Ortga"), types.KeyboardButton('Ovqat'),
			types.KeyboardButton('Maxsulot'))
		bot_message = bot.send_message(message.from_user.id,'Hozirdagi bosh honalar Buyurtma berish uchun honani tanlang!', reply_markup=room_markup)
		bot.register_next_step_handler(bot_message, order_delivery_controller, query , name)



def order_controller(message, date, phone, name):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		room = message.text
		data = {
			"name": name,
			"room": room,
			"phone": phone,
			"date": date
		}
		query = requests.post(f'{base_url}/create-order/', data=data).json()
		if query['status'] == 200:
			bot.send_message(message.from_user.id, 'Buyurtmangiz muvofaqiyatli berildi!', reply_markup=markup)
		elif query['status'] == 500:
			bot.send_message(message.from_user.id, 'Buyurtmangiz berishdagi hatolik!', reply_markup=markup)
		else:
			bot.send_message(message.from_user.id, 'Hatolik!', reply_markup=markup)


def order_delivery_controller(message, phone,  name):
	if message.text == "Ortga":
		send_welcome(message)
	else:
		data = {
			"name": name,
			'date':message.text,
			"phone": phone,
		}
		query = requests.post(f'{base_url}/create-delivery/', data=data).json()
		print(query)
		print(query['status'])
		if query['status'] == 200:
			bot.send_message(message.from_user.id, 'Buyurtmangiz muvofaqiyatli berildi!', reply_markup=markup)
		elif query['status'] == 500:
			bot.send_message(message.from_user.id, 'Buyurtmangiz berishdagi hatolik!', reply_markup=markup)
		else:
			bot.send_message(message.from_user.id, 'Hatolik!', reply_markup=markup)


bot.infinity_polling()
