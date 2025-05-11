
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==== تنظیمات ====
TOKEN = '7572798086:AAH_KiCmdlS-9UywvSTmNWF2MQfggxgv7ME'
ADMIN_ID = 7427163453
CHANNEL_USERNAME = '@Linearpark1'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_user_message(message):
    if message.chat.type == 'private':
        user_id = message.chat.id
        username = message.from_user.username or "ندارد"

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("✅ تایید", callback_data=f"approve:{user_id}:{message.message_id}"),
            InlineKeyboardButton("❌ رد", callback_data="reject")
        )

        msg_text = f"📩 پیام جدید:

{message.text}

👤 از: @{username} (ID: {user_id})"
        bot.send_message(ADMIN_ID, msg_text, reply_markup=markup)
        bot.send_message(user_id, "✅ پیام شما دریافت شد و منتظر تایید ادمین است.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve:") or call.data == "reject")
def handle_callback(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "شما ادمین نیستید.")
        return

    if call.data.startswith("approve:"):
        parts = call.data.split(":")
        original_message = call.message.text.split("\n\n")[1].split("\n")[0]
        bot.send_message(CHANNEL_USERNAME, f"📝 پیام ناشناس:

{original_message}")
        bot.answer_callback_query(call.id, "✅ پیام ارسال شد به کانال.")

    elif call.data == "reject":
        bot.answer_callback_query(call.id, "❌ پیام رد شد.")

print("ربات اجرا شد...")
bot.infinity_polling()
