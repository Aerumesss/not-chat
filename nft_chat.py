import os
import asyncio
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_USERNAMES = ['@NftProdazha1', '@NftProdazha3', '@NftProdazha4']
MESSAGE = 'Не забудь заглянуть магазин нфт подарков @AxegarovShop'
INTERVAL = 2 * 60  # 2 минуты

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("▶️ Запустить рассылку", callback_data='start_sending')],
        [InlineKeyboardButton("⏹️ Остановить рассылку", callback_data='stop_sending')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start_sending':
        if not context.bot_data.get('is_sending', False):
            context.bot_data['is_sending'] = True
            await query.edit_message_text('✅ Рассылка запущена!')
            asyncio.create_task(send_messages_loop(context.bot, context))
        else:
            await query.edit_message_text('🔁 Рассылка уже работает.')
    elif query.data == 'stop_sending':
        context.bot_data['is_sending'] = False
        await query.edit_message_text('⏹️ Рассылка остановлена.')

async def send_messages_loop(bot: Bot, context: ContextTypes.DEFAULT_TYPE):
    while context.bot_data.get('is_sending', False):
        for chat in CHAT_USERNAMES:
            try:
                await bot.send_message(chat_id=chat, text=MESSAGE)
                logger.info(f"✅ Сообщение отправлено в {chat}")
            except Exception as e:
                logger.error(f"⚠️ Ошибка отправки в {chat}: {e}")
        await asyncio.sleep(INTERVAL)

def main():
    # Создаем новый event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        
        logger.info("🚀 Бот запущен")
        app.run_polling()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
