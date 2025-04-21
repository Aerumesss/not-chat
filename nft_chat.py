import os
import asyncio
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная окружения BOT_TOKEN не установлена!")

# Настройки рассылки
CHAT_USERNAMES = ['@NftProdazha1', '@NftProdazha3', '@NftProdazha4']
MESSAGE = 'Не забудь заглянуть магазин нфт подарков @AxegarovShop'
INTERVAL = 2 * 60  # 2 минуты

# Флаг рассылки
is_sending = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("▶️ Отправить сообщения", callback_data='start_sending')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_sending
    query = update.callback_query
    await query.answer()

    if query.data == 'start_sending':
        if not is_sending:
            is_sending = True
            await query.edit_message_text('✅ Рассылка запущена! Каждые 2 минуты будет отправлено сообщение.')
            asyncio.create_task(send_messages_loop(context.bot))
        else:
            await query.edit_message_text('🔁 Рассылка уже работает.')

async def send_messages_loop(bot: Bot):
    global is_sending
    while is_sending:
        for chat in CHAT_USERNAMES:
            try:
                await bot.send_message(chat_id=chat, text=MESSAGE)
                print(f"✅ Сообщение отправлено в {chat}")
            except Exception as e:
                print(f"⚠️ Ошибка отправки в {chat}: {e}")
        await asyncio.sleep(INTERVAL)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Бот запущен")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
