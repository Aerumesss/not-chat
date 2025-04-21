import asyncio
import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("7535199249:AAHJnhqPj08EvntQqGoxGZrEpCFqfHJ2Yi8")  # Не храни токен в коде!
WEBHOOK_PATH = "/webhook"
WEBHOOK_PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

CHAT_USERNAMES = ['@NftProdazha1', '@NftProdazha3', '@NftProdazha4']
MESSAGE = 'Не забудь заглянуть магазин нфт подарков @AxegarovShop'
INTERVAL = 2 * 60

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
                print(f"Сообщение отправлено в {chat}")
            except Exception as e:
                print(f"Ошибка отправки в {chat}: {e}")
        await asyncio.sleep(INTERVAL)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Установка webhook
    await app.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")

    # Запуск webhook-сервера
    await app.run_webhook(
        listen="0.0.0.0",
        port=WEBHOOK_PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    asyncio.run(main())
