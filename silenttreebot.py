import telebot
import time

TOKEN = '8417048578:AAHynDtRP6mpVPnIT9uhvsKyyq9bChDZhbA'
GROUP_CHAT_ID = -1002413106992
THREAD_ID = 8  # ID темы форума

bot = telebot.TeleBot(TOKEN)

# Для антиспама
last_sent = {}

SPAM_DELAY = 30  # секунд

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📥 Подать заявку", "🚫 Оставить жалобу")
    bot.send_message(message.chat.id, "Привет! Выбери действие:", reply_markup=markup)

def is_spam(user_id):
    now = time.time()
    if user_id in last_sent and now - last_sent[user_id] < SPAM_DELAY:
        return True
    last_sent[user_id] = now
    return False

@bot.message_handler(func=lambda msg: msg.text == "📥 Подать заявку")
def ask_form(msg):
    if is_spam(msg.from_user.id):
        bot.send_message(msg.chat.id, "⏳ Пожалуйста, подождите перед следующей отправкой.")
        return
    bot.send_message(msg.chat.id,

        "Анкета для флуда\n\n"
        "1. [Ваша роль] - [юз] \n"
        "2. [Ваш часовой пояс (от мск)] \n"
        "3. [Дата рождения (день, месяц)]",
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, forward_form)

@bot.message_handler(func=lambda msg: msg.text == "🚫 Оставить жалобу")
def ask_complaint(msg):
    if is_spam(msg.from_user.id):
        bot.send_message(msg.chat.id, "⏳ Пожалуйста, подождите перед следующей отправкой.")
        return
    bot.send_message(msg.chat.id, "Напиши жалобу в одном сообщении:", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, forward_complaint)

def forward_form(msg):
    user = f"@{msg.from_user.username}" if msg.from_user.username else msg.from_user.first_name
    text = f"📨 Анкета от {user}:\n\n{msg.text.strip()}"
    bot.send_message(chat_id=GROUP_CHAT_ID, text=text, message_thread_id=THREAD_ID)
    bot.send_message(msg.chat.id, "✅ Анкета отправлена!\nПодайте заявку на вступление и ожидайте\nhttps://t.me/+IR9Oi62rBtIyMzI6")

def forward_complaint(msg):
    user = f"@{msg.from_user.username}" if msg.from_user.username else msg.from_user.first_name
    text = f"🚫 Жалоба от {user}:\n\n{msg.text.strip()}"
    bot.send_message(chat_id=GROUP_CHAT_ID, text=text, message_thread_id=THREAD_ID)
    bot.send_message(msg.chat.id, "✅ Жалоба отправлена!")

bot.infinity_polling()
