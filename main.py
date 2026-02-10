import telebot
import requests
import os

BOT_TOKEN = "8500831062:AAGdcSMnsKkxZYs3HRqOZcGtAWZOOafdaI4"
CHANNEL ="AI-GENERATED"   # kanaling username
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(8500831062:AAGdcSMnsKkxZYs3HRqOZcGtAWZOOafdaI4)

# obuna tekshirish
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member","creator","administrator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not check_sub(message.from_user.id):
        bot.reply_to(message,
        f"❌ To use bot subscribe first:\n{CHANNEL}\n\n"
        f"❌ Чтобы пользоваться ботом подпишись:\n{CHANNEL}")
        return
    
    bot.reply_to(message,
    "🍔 Send food name for recipe\n🍔 Напиши еду для рецепта")

@bot.message_handler(func=lambda message: True)
def reply(message):
    if not check_sub(message.from_user.id):
        bot.reply_to(message,
        f"Subscribe first: {CHANNEL}\nСначала подпишись: {CHANNEL}")
        return

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": """You are elite chef AI.
Always reply in English and Russian.
Give detailed recipes and cooking tips.
English first then Russian."""
            },
            {"role": "user", "content": message.text}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    answer = response.json()["choices"][0]["message"]["content"]

    bot.reply_to(message, answer)

bot.polling()
