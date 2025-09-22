from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os, time

# 🔑 Берём токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

BAD_WORDS = ["спам", "реклама", "флуд", "xxx", "http://", "https://"]

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Я бот-модератор. Добавь меня в чат и дай права администратора!")

def check_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    user = update.message.from_user

    if any(word in text for word in BAD_WORDS):
        try:
            update.message.delete()
            update.message.reply_text(f"⚠️ {user.first_name}, сообщение удалено. Нарушение правил!")
        except:
            pass

def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"👋 Добро пожаловать, {member.first_name}!")

def mute(update: Update, context: CallbackContext):
    try:
        user = update.message.reply_to_message.from_user
        chat = update.message.chat
        chat.restrict_member(
            user.id,
            ChatPermissions(can_send_messages=False),
            until_date=int(time.time()) + 60
        )
        update.message.reply_text(f"🔇 {user.first_name} замучен на 1 минуту.")
    except:
        update.message.reply_text("❌ Ошибка. Бот должен быть админом.")

def ban(update: Update, context: CallbackContext):
    try:
        user = update.message.reply_to_message.from_user
        chat = update.message.chat
        chat.kick_member(user.id)
        update.message.reply_text(f"⛔️ {user.first_name} забанен.")
    except:
        update.message.reply_text("❌ Ошибка. Бот должен быть админом.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("ban", ban))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()
