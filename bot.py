import logging
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext, ContextTypes

# Вставьте сюда ваш токен бота
TOKEN = '7170984511:AAF4LPEwQ6iEIEyW4CZyJ_PP_sXqrMfTTec'
WEBSITE_URL = 'http://127.0.0.1:8000/'  # URL вашего сайта для обработки запросов

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот поддержки вашего сайта. Как я могу помочь вам?')

# Команда /get_users
async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Отправка запроса на ваш сайт для получения списка пользователей
    response = requests.get('http://127.0.0.1:8000/api/v1/accounts/')

    if response.status_code == 200:
        users = response.json().get('users', [])
        if users:
            users_text = '\n'.join(users)
            await update.message.reply_text(f'Список пользователей:\n{users_text}')
        else:
            await update.message.reply_text('На сайте нет зарегистрированных пользователей.')
    else:
        await update.message.reply_text('Произошла ошибка при получении списка пользователей.')

# Обработка ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main() -> None:
    # Создание приложения
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('get_users', get_users))
    application.add_error_handler(error)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
