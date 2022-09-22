import logging
import aiogram
import qrcode
import requests
import os
import threading

from db import db, create_db
from random import randint

from aiogram.utils.deep_linking import decode_payload
from aiogram.utils.deep_linking import get_start_link
from aiogram.types import Message

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

token = "5653477884:AAGQC90jz5EPbRvxlUm5EvGziASZ_DQmdrg" #СЮДА ТОКЕН

wallet_QIWI = "79889912552" #СЮДА НОМЕР КИВИ
wallet_BTC = "bc1qm2v6jkykxkzwn0yucn7ywzmn9hmc8hv47p8sxh" #СЮДА КОШЕЛЕК БТК

admin_id = "5352228966" # СЮДА АЙДИ АДМИНА

cities = [
    "Москва",
    "Санкт-Петербург",
    "Адлер",
    "Анапа",
    "Абакан",
    "Альметьевск",
    "Ангарск",
    "Арзамас",
    "Армавир",
    "Архангельск",
    "Ачинск",
    "Балаково",
    "Балашиха",
    "Батайск",
    "Белгород",
    "Бердск",
    "Бийск",
    "Благовещенск",
    "Братск",
    "Брянск",
    "Владикавказ",
    "Владимир",
    "Волжский",
    "Воронеж",
    "Волгоград",
    "Владивосток",
    "Великий Новгород",
    "Грозный",
    "Дзержинск",
    "Домодедово",
    "Евпатория",
    "Екатеринбург",
    "Железногорск",
    "Иваново",
    "Ижевск",
    "Йошка-Ола",
    "Иркутск",
    "Калининград",
    "Калуга",
    "Казань",
    "Каменск-Уральский",
    "Каспийск",
    "Кемерово",
    "Керчь",
    "Киров",
    "Кисловодск",
    "Коломна",
    "Красногорск",
    "Краснодар",
    "Красноярск",
    "Курган",
    "Курск",
    "Кызыл",
    "Липецк",
    "Люберцы",
    "Магнитогорск",
    "Майкоп",
    "Махачкала",
    "Мурманск",
    "Мытище",
    "Назрань",
    "Нальчик",
    "Находка",
    "Нижний Новгород",
    "Нижний Тагил",
    "Новокузнецк",
    "Новосибирск",
    "Норильск",
    "Новый Уренгой",
    "Одинцово",
    "Обнинск",
    "Омск",
    "Орёл",
    "Оренбург",
    "Орехово-Зуево",
    "Орск",
    "Пенза",
    "Пермь",
    "Петразаводск",
    "Подольск",
    "Прокопьевск",
    "Псков",
    "Пушкино",
    "Пятигорск",
    "Раменское",
    "Ростов-На-Дону",
    "Рыбинск",
    "Рязань",
    "Салават",
    "Самара",
    "Саранск",
    "Саратов",
    "Севастопаль",
    "Симферополь",
    "Смоленск",
    "Сочи",
    "Ставрополь",
    "Старый осколок",
    "Сургут",
    "Сызрань",
    "Сыктывкар",
    "Таганрог",
    "Тамбов",
    "Тверь",
    "Тольятти",
    "Томск",
    "Тула",
    "Тюмень",
    "Туапсе",
    "Улан-Удэ",
    "Ульяновск",
    "Уссурийск",
    "Уфа",
    "Хабаровск",
    "Хасавюрт",
    "Химки",
    "Чебоксары",
    "Челябинск",
    "Череповец",
    "Черкесск",
    "Чита",
    "Шахты",
    "Щелково",
    "Энгельс",
    "Якутск",
    "Ярославль",
    "Ялта"
]

stuffs = [
    "🍫 Гашиш (ice-o-later) - 1гр 2000₽",
    "🍫 Гашиш (ice-o-later) - 5гр 8000₽",
    "🍫 Гашиш (ice-o-later) - 10гр 12500₽",
    "🌳 Бошки (OG Kush) - 1гр 1900₽",
    "🌳 Бошки (OG Kush) - 2гр 3500₽",
    "🌳 Бошки (OG Kush) - 5гр 7000₽",
    "🧊 Скорость A-PVP - 0,5гр 1600₽",
    "🧊 Скорость A-PVP - 1гр 2900₽",
    "🧊 Скорость A-PVP - 5гр 9000₽",
    "💎 Мефедрон (крис) - 0,5гр 1650₽",
    "💎 Мефедрон (крис) - 1гр 2950₽",
    "💎 Мефедрон (крис) - 5гр 12000₽",
    "🌫 Амфетамин - 1гр 2550₽",
    "🌫 Амфетамин - 2гр 4700₽",
    "🍭 Экстази (Red Bull) - 5шт 6000₽",
    "🍭 Экстази (Red Bull) - 10шт 10000₽",
    "🍭 Экстази (Red Bull) - 20шт 15000₽",
    "💥 Героин 666 - 0.5гр 2800₽",
    "💥 Героин 666 - 1гр 4900₽",
    "💥 Героин 666 - 5гр 15000₽",
    "🌈 LSD 220 mkg - 1шт 1150₽",
    "🌈 LSD 220 mkg - 2шт 2000₽",
    "🌈 LSD 220 mkg - 3шт 3600₽",
    "💊 Лирика 300 - 1 лист 3850₽"
]

treasures = [
    "🧲 Магнит",
    "⛳️ Прикоп"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


def rate(amount): 
    s = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym=RUB&tsyms=BTC")
    raw = s.json()

    BTC = float(raw["BTC"]) * float(amount)

    return [BTC]

def order_pay():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_1 = types.KeyboardButton(text="QIWI")
    btn_2 = types.KeyboardButton(text="Bitcoin")

    keyboard.add(btn_1, btn_2)

    return keyboard

async def starting(user_id, user_un):
    if not db.user_exists(user_id):
        db.add_user(user_id)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_1 = types.KeyboardButton(text="🎁 Купить товар")
    btn_2 = types.KeyboardButton(text="📝 Правила")
    btn_3 = types.KeyboardButton(text="🔔 Поддержка")

    keyboard.add(btn_1, btn_2, btn_3)

    await bot.send_message(text=f"🎊 Спасибо {user_un} что выбрали наш магазин.\n\n"
                                 "👊 Приятных покупок и легких подъёмов!", chat_id=user_id, reply_markup=keyboard)

async def choose(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for stuff in stuffs: 
        btn = types.KeyboardButton(text=stuff)
        keyboard.add(btn)

    back = types.KeyboardButton(text="🔙 Назад")
    keyboard.add(back)

    await bot.send_message(text=f"Выберите товар 🍬", chat_id=user_id, reply_markup=keyboard)

async def district(user_id, user_un):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text="🔙 Назад")
    keyboard.add(back)

    await bot.send_message(text=f"{user_un} укажите ваш район или улицу, по этим данным бот подберёт вам ближайший адрес закладки и после оплаты позже выдаст полную информацию: фото+координаты+описание.\n\n"
                                f"Пример: Северный район, улица Карамзина\n\n"
                                f"❗️Если Вы НЕВЕРНО указываете район или улицу, то адрес будет выбран рандомно (случайно) в указанном Вами городе.❗️\n\n", chat_id=user_id, reply_markup=keyboard)

async def hide(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for treasure in treasures: 
        btn = types.KeyboardButton(text=treasure)
        keyboard.add(btn)

    back = types.KeyboardButton(text="🔙 Назад")
    keyboard.add(back)

    await bot.send_message(text=f"Выберите вид клада", chat_id=user_id, reply_markup=keyboard)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_un = message.from_user.username
    
    args = message.get_args()
    payload = decode_payload(args)
    if not payload == "":
        if user_un is None:
            await bot.send_message(text=f"<b>🪄 Новый пользователь c реферальной ссылки!</b>\n"
                                        f"<b>🙌🏻 Реферальная ссылка:</b> <code>{payload}</code>\n\n"
                                        f"<b>🆔 Айди:</b> <a href='tg://user?id={user_id}'>{user_id}</a>\n", chat_id=admin_id, parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(text=f"<b>🪄 Новый пользователь c реферальной ссылки!</b>\n"
                                        f"<b>🙌🏻 Реферальная ссылка:</b> <code>{payload}</code>\n\n"
                                        f"<b>🆔 Айди:</b> <a href='tg://user?id={user_id}'>{user_id}</a>\n"
                                        f"<b>👤 Юзернейм: @{user_un}</b>\n", chat_id=admin_id, parse_mode=types.ParseMode.HTML)


    await starting(user_id, user_un)

@dp.message_handler(text=["🔙 Назад", "🔙 Отмена"])
async def back(message: types.Message):
    user_id = message.from_user.id
    user_un = message.from_user.username
    
    await starting(user_id, user_un)

@dp.message_handler(text=["🎁 Купить товар"])
async def rules(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for city in cities: 
        btn = types.KeyboardButton(text=city)
        keyboard.add(btn)

    back = types.KeyboardButton(text="🔙 Назад")
    keyboard.add(back)

    await message.answer(text="🏙️ Выберите город\n\n"
                              "(К сожалению в данный момент клады только в России)", reply_markup=keyboard)

@dp.message_handler(text=["📝 Правила"])
async def rules(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text="🔙 Назад")
    keyboard.add(back)

    await message.answer(text="1) Не хамить и не оскорблять сотрудников магазина в спорных вопросах!\n\n"
                              "2) Если у вас случился ненаход, то Вы должны предоставить не менее 2-ух фото в течении 24-х часов с момента покупки!\n\n"
                              "3) Если у вас недовес, Вы должны предоставить видеодоказательство вскрытия пака, фото стаффа на весах без зипа, а также фото любой монеты на весах!\n\n"
                              "4) Передача адреса третьим лицам запрещена!\n\n"
                              "Приятных покупок!", reply_markup=keyboard)

@dp.message_handler(text=["🔔 Поддержка"])
async def rules(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton(text="🔙 Назад")
    keyboard.add(btn_1)

    await message.answer(text="Если возникли какие то проблемы - пишите\n\n"
                              "@Operator_Anya", reply_markup=keyboard)

# АДМИН
@dp.message_handler(chat_type=[types.ChatType.PRIVATE], commands="admin")
async def admin(message: types.Message):
    user_id = message.from_user.id
    user_un = message.from_user.full_name

    if str(user_id) == str(admin_id):
        await bot.send_message(text=f"<b>🎗 Добро пожаловать {user_un}!</b>\n\n"
                                    f"👁 /make – <b>Создать реферальную ссылку</b>  <code>(Пример: /make текст)</code>\n"
                                    f"📊 /stats – <b>Статистика</b>\n"
                                    f"📄 /send – <b>Рассылка</b> <code>(Пример: /send текст)</code>", chat_id=user_id, parse_mode=types.ParseMode.HTML)

@dp.message_handler(chat_type=[types.ChatType.PRIVATE], commands="stats")
async def stats(message: types.Message):
    user_id = message.from_user.id

    if str(user_id) == str(admin_id):
        await bot.send_message(text=f"<b>🪄 Статистика:</b>\n\n"
                                    f"<b>🟩 Активные пользователи:</b> <code>{db.get_all_users()[0][0]}</code>\n"
                                    f"<b>🟥 Не активные пользователи:</b> <code>{db.get_no_active_users()[0][0]}</code>", chat_id=user_id, parse_mode=types.ParseMode.HTML)

@dp.message_handler(chat_type=[types.ChatType.PRIVATE], commands="send")
async def send(message: types.Message):
    user_id = message.from_user.id

    if str(user_id) == str(admin_id):
        if message.text == "/send":
            await bot.send_message(text=f"<b>Окей, а что писать им?..</b>", chat_id=user_id, parse_mode=types.ParseMode.HTML) 

            return

        text = message.text[len("/send "):]
        
        users = db.get_users()
        active = 0
        no_active = 0
        for row in users:
            try:
                await bot.send_message(row[0], text, parse_mode=types.ParseMode.HTML) 

                if int(row[1]) != 1:
                    db.set_active(row[0], 1)

                active = active + 1
            except:
                db.set_active(row[0], 0)
                no_active = no_active + 1

                continue
        
        await bot.send_message(text=f"<b>🎉 Рассылка успешно завершена!</b>\n\n"
                                    f"<b>🎊 Отправлено:</b> <code>{active}</code>\n"
                                    f"<b>📛 Не отправлено:</b> <code>{no_active}</code>", chat_id=user_id, parse_mode=types.ParseMode.HTML)

@dp.message_handler(chat_type=[types.ChatType.PRIVATE], commands="make")
async def make(message: types.Message):
    user_id = message.from_user.id

    if str(user_id) == str(admin_id):
        if message.text == "/make":
            await bot.send_message(text=f"<b>Окей, а как назвать реферальную ссылку?..</b>", chat_id=user_id, parse_mode=types.ParseMode.HTML) 

            return

        text = message.text[len("/make "):]
        
        link = await get_start_link(text, encode=True)
        
        await bot.send_message(text=f"<b>🎉 Реферальная ссылка успешно создана!</b>\n\n"
                                    f"<b>🎊 Ссылка:</b> <code>{link}</code>\n"
                                    f"<b>💬 Название:</b> <code>{text}</code>", chat_id=user_id, parse_mode=types.ParseMode.HTML)

# ПРОЧЕЕ
@dp.message_handler(text=["QIWI"])
async def type_pay(message: types.Message):
    user_id = message.from_user.id
    #link = f"<a href='https://qiwi.com/payment/form/99?amountInteger=1111&amountFraction=0&currency=643&extra['comment']=222&extra['account']={wallet_QIWI}&blocked[0]=sum&blocked[1]=comment&blocked[2]=account'>оплатить</a>"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    check = types.KeyboardButton(text="🔎 Получить информацию по адресу")
    back = types.KeyboardButton(text="🔙 Отмена")
    keyboard.add(check, back)

    await message.answer(text=f"1️⃣ Способ оплаты:\n"
                              f"➖ QIWI\n\n"
                              f"Сумма платежа должна быть равна цене товара или больше, иначе бот не зафиксирует оплату.\n\n"
                              f"2️⃣ После оплаты предоставьте боту для проверки платежа фотографию чека либо скриншот.\n\n"
                              f"3️⃣ Если все условия выполнены, ожидайте! Проверка займет от 2ух до 5ти минут, после чего бот вышлет вам полную информацию по адресу.\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖\n"
                              f"🥝 QIWI кошелек: <code>{wallet_QIWI}</code>\n"
                              
                              
                            # f"{link}"
                              f"➖➖➖➖➖➖➖➖➖➖➖\n\n"
                              f"❗️ Если остались какие-то вопросы, вы можете обратиться к нашему ОПЕРАТОРУ за консультацией❗️\n"
                              f"➡️ @Operator_Anya\n\n"
                              f"👍 Приятного время провождения и легкого подъёма!" ,reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

@dp.message_handler(text=["Bitcoin"])
async def type_pay(message: types.Message):
    user_id = message.from_user.id

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    check = types.KeyboardButton(text="🔎 Получить информацию по адресу")
    back = types.KeyboardButton(text="🔙 Отмена")
    keyboard.add(back)

    file_path = str(user_id)+".png"
    qrcode_gen = qrcode.make(f"bitcoin: {wallet_BTC}")
    qr = qrcode_gen.save(file_path)

    await message.answer_photo(caption=f"1️⃣ Способ оплаты:\n"
                                       f"➖ BITCOIN\n\n"
                                       f"Сумма платежа должна быть равна цене товара или больше, иначе бот не зафиксирует оплату.\n\n"
                                       f"2️⃣ После оплаты предоставьте боту для проверки платежа фотографию чека либо скриншот.\n\n"
                                       f"3️⃣ Если все условия выполнены, ожидайте! Проверка займет от 2ух до 5ти минут, после чего бот вышлет вам полную информацию по адресу.\n"
                                       f"➖➖➖➖➖➖➖➖➖➖➖\n"
                                       f"🥝 Bitcoin: <code>{wallet_BTC}</code>\n"
                                       f"➖➖➖➖➖➖➖➖➖➖➖\n\n"
                                       f"❗️ Если остались какие-то вопросы, вы можете обратиться к нашему ОПЕРАТОРУ за консультацией❗️\n"
                                       f"➡️ @Operator_Anya\n\n"
                                       f"👍 Приятного время провождения и легкого подъёма!", photo=open(file_path, 'rb'), reply_markup=keyboard, parse_mode="HTML")
    os.remove(file_path)

@dp.message_handler(text=["🔎 Получить информацию по адресу"])
async def check_pay(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton(text="🔙 Отмена")
    keyboard.add(back)

    await message.answer(text="🧾 Отправьте в чат боту фото, либо скриншот чека об оплате!", reply_markup=keyboard)

@dp.message_handler()
async def start(message: types.Message):
    user_id = message.from_user.id
    user_un = message.from_user.username

    if user_un is None:
        user_un = message.from_user.full_name
    
    if message.text in cities:
        await choose(user_id)
    elif message.text in stuffs:
        await district(user_id, user_un)
    elif message.text in treasures:
        await message.answer(text="Выберите способ оплаты", reply_markup=order_pay())
    elif message.text:
        await hide(user_id)

async def on_startup(dispatcher):
    create_db()

def anti_sleep():
	while True:
		try:
			randomic = random.randint(0, 10)
			time.sleep(1200)
		except:
			pass
		

if __name__ == '__main__':
    x1 = threading.Thread(target=anti_sleep, args=())
    x1.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
