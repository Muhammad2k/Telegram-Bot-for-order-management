from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from database import save_info

TOKEN = "7705727576:AAFCF7teIpgBRhn5M_35uSKWUpJaULuyHb0"
channel_name = "@ssszayavki"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or message.text == '/start' or message.text == 'Zayavka goldirish':
        await start(message)
    elif 'name' not in user_data[user_id]:
        await ask_phone(message)
    elif 'phone' not in user_data[user_id]:
        await ask_age(message)
    elif 'age' not in user_data[user_id]:
        await total_info(message)

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.answer("Assalomu alaykum! \nIltimos ismingizni kiriting:")
    print(user_data)

async def ask_phone(message: types.Message):
    user_id = message.from_user.id
    name = message.text
    user_data[user_id]['name'] = name
    button = [
        [types.KeyboardButton(text="Raqam jo'natish", request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer("Iltimos telefon raqamingizni kiriting:", reply_markup=keyboard)
    print(user_data)

async def ask_age(message: types.Message):
    user_id = message.from_user.id
    if message.contact is not None:
         phone = message.contact.phone_number
    else:
        phone = message.text
    user_data[user_id]['phone'] = phone
    await message.answer("Iltimos yoshingizni kiriting:")
    print(user_data)

async def total_info(message: types.Message):
    user_id = message.from_user.id
    age = message.text
    user_data[user_id]['age'] = age
    button = [
        [types.KeyboardButton(text="Zayavka goldirish")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    name = user_data[user_id]['name']
    phone = user_data[user_id]['phone']
    message_text = (f"Ismingiz: {name}\n"
                    f"Yoshingiz: {age}\n"
                    f"Telefon raqamiz: {phone}")
    save_info(user_id, name, phone, age)
    await message.answer(f"Zayavkangiz qabul qilindi\n{message_text}", reply_markup=keyboard)
    await bot.send_message(channel_name, message_text)
    print(user_data)
    del user_data[user_id]
    print(user_data)

async def main():
    await dp.start_polling(bot)

print ('The bot is running...')
asyncio.run(main())