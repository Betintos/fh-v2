import telebot
from telebot import types
import requests
# Импортируются необходимые библиотеки: telebot для работы с Telegram API, types для создания различных типов сообщений, и requests для выполнения HTTP-запросов.



token = '7170984511:AAF4LPEwQ6iEIEyW4CZyJ_PP_sXqrMfTTec'
bot = telebot.TeleBot(token)
#oken: Это уникальный токен, который используется для аутентификации вашего бота с Telegram API. Его вы получаете от BotFather в Telegram.
#bot: Создается экземпляр класса TeleBot, который используется для взаимодействия с Telegram API.



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """Привет! Я бот Instagram.
Нажмите на следующую команду для дальнейшей работы:
/Ytub""")
#@bot.message_handler(commands=['start']): Это декоратор, который говорит боту, что функция start_message должна быть вызвана, 
#когда пользователь отправляет команду /start.
#start_message(message): Функция, которая будет вызвана, когда команда /start получена. Она отправляет приветственное сообщение пользователю.



@bot.message_handler(commands=['Ytub'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Video")
    item2 = types.KeyboardButton("Comments")
    item3 = types.KeyboardButton("Users")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
#@bot.message_handler(commands=['inst']): Это декоратор, который говорит боту, что функция button_message должна быть вызвана, когда пользователь отправляет команду /inst.
# button_message(message): Функция, которая будет вызвана, когда команда /inst получена. Она создает клавиатуру с тремя кнопками: "Посты", "Отзывы" и "Пользователи".
# types.ReplyKeyboardMarkup(resize_keyboard=True): Создается клавиатура, которая автоматически подстраивается под размер экрана.
# types.KeyboardButton("Посты"), types.KeyboardButton("Отзывы"), types.KeyboardButton("Пользователи"): Создаются кнопки.
# markup.add(item1, item2, item3): Добавление кнопок в клавиатуру.
# bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup): Отправка сообщения с созданной клавиатурой.
@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Video":
        response = requests.get('http://34.16.210.117/api/v1/videos/')
        if response.status_code == 200:
            bot.send_message(message.chat.id, f'Информация о постах:\n{response.text}')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка при получении информации о постах.')
    elif message.text == "Comments":
        response = requests.get('http://34.16.210.117/api/v1/comments/')
        if response.status_code == 200:
            bot.send_message(message.chat.id, f'Информация об отзывах:\n{response.text}')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка при получении отзывов.')
    elif message.text == "Users":
        response = requests.get('http://34.16.210.117/api/v1/accounts/')
        if response.status_code == 200:
            bot.send_message(message.chat.id, f'Информация о пользователях:\n{response.text}')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка при получении информации о пользователях.')
#@bot.message_handler(content_types=['text']): Это декоратор, который говорит боту, что функция message_reply должна быть вызвана, когда бот получает текстовое сообщение.
# message_reply(message): Функция, которая будет вызвана, когда получено текстовое сообщение. В зависимости от текста сообщения, выполняется определенное действие:
# Если текст сообщения "Посты", "Отзывы" или "Пользователи", бот делает соответствующий HTTP-запрос к указанному API.
# requests.get(url): Выполняется GET-запрос к указанному URL.
# response.status_code == 200: Проверяется, успешен ли запрос (код ответа 200 означает успех).
# bot.send_message(message.chat.id, f'Информация о постах:\n{response.text}'): Отправка полученной информации пользователю. Если запрос неуспешен, отправляется сообщение об ошибке.




bot.infinity_polling()