from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# 👉 ВСТАВЬ СЮДА СВОЙ ТОКЕН
BOT_TOKEN = '8184463577:AAE7-ghOSl-tLDH1xohVm-iVy3PPnoQZwNU'

# 👉 ВСТАВЬ ID ЧЕЛОВЕКА/ЧАТА, КУДА ОТПРАВЛЯТЬ ДЕМКИ (можно узнать через @userinfobot)
DESTINATION_CHAT_ID = 1874218277


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🎧 Отправь сюда свою демку (mp3, wav, голосовое или файл) — и мы её послушаем!"
    )


async def handle_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message = update.message
    file = message.audio or message.voice or message.document

    if not file:
        await message.reply_text("Пожалуйста, отправь аудио файл, голосовое или документ с треком.")
        return

    caption = f"🎶 Новая демка от @{user.username or user.first_name} (ID: {user.id})"

    try:
        if message.audio:
            await context.bot.send_audio(chat_id=DESTINATION_CHAT_ID, audio=file.file_id, caption=caption)
        elif message.voice:
            await context.bot.send_voice(chat_id=DESTINATION_CHAT_ID, voice=file.file_id, caption=caption)
        elif message.document:
            await context.bot.send_document(chat_id=DESTINATION_CHAT_ID, document=file.file_id, caption=caption)

        await message.reply_text("Спасибо! Твоя демка отправлена лейблу. 🔥")
    except Exception as e:
        await message.reply_text("Произошла ошибка при отправке демки. Попробуй ещё раз позже.")
        print(f"Ошибка при отправке демки: {e}")


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.Document.AUDIO, handle_demo))

    print("✅ Бот запущен. Ожидаю демки...")
    app.run_polling()
