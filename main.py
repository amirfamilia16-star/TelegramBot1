import telebot
from telebot import types
import google.generativeai as genai
import json
import os
import random

from config import BOT_TOKEN, GEMINI_API_KEY

bot = telebot.TeleBot(BOT_TOKEN)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("👤 О себе")
    btn2 = types.KeyboardButton("🎯 Моя цель")
    btn3 = types.KeyboardButton("📖 История")
    btn4 = types.KeyboardButton("🧑‍🏫 Ментор")
    btn5 = types.KeyboardButton("📈 Прогресс")
    btn6 = types.KeyboardButton("🎮 Хобби")
    btn7 = types.KeyboardButton("💼 Работы")
    btn8 = types.KeyboardButton("🌐 GitHub")
    btn9 = types.KeyboardButton("🤖 AI Чат")
    btn10 = types.KeyboardButton("🎵 Мои любимые песни")
    btn11 = types.KeyboardButton("🎵 Мой TikTok")
    btn12 = types.KeyboardButton("💰 ИИ Бизнесмен")
    btn13 = types.KeyboardButton("🎧 Найти музыку")
    

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7, btn8)
    markup.add(btn9)
    markup.add(btn10)
    markup.add(btn11)
    markup.add(btn12)
    markup.add(btn13)

    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в мое портфолио!",
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, data["about"])

@bot.message_handler(commands=["goal"])
def goal(message):
    bot.send_message(message.chat.id, data["goal"])

@bot.message_handler(commands=["story"])
def story(message):
    bot.send_message(message.chat.id, data["story"])

@bot.message_handler(commands=["mentor"])
def mentor(message):
    bot.send_message(message.chat.id, data["mentor"])

@bot.message_handler(commands=["progress"])
def progress(message):
    bot.send_message(message.chat.id, data["progress"])

@bot.message_handler(commands=["hobby"])
def hobby(message):
    bot.send_message(message.chat.id, data["hobby"])

@bot.message_handler(commands=["works"])
def works(message):
    bot.send_message(message.chat.id, data["works"])

@bot.message_handler(commands=["github"])
def github(message):
    bot.send_message(message.chat.id, data["github"])

@bot.message_handler(commands=["mem"])
def mem(message):
    try:
        folder = "screenshots"

        photos = [
            os.path.join(folder, file)
            for file in os.listdir(folder)
            if file.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if not photos:
            bot.send_message(message.chat.id, "Фотографии не найдены.")
            return

        photo = random.choice(photos)

        with open(photo, "rb") as img:
            bot.send_photo(message.chat.id, img)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

@bot.message_handler(func=lambda message: message.text == "👤 О себе")
def btn_about(message):
    bot.send_message(message.chat.id, data["about"])

@bot.message_handler(func=lambda message: message.text == "🎯 Моя цель")
def btn_goal(message):
    bot.send_message(message.chat.id, data["goal"])

@bot.message_handler(func=lambda message: message.text == "📖 История")
def btn_story(message):
    bot.send_message(message.chat.id, data["story"])

@bot.message_handler(func=lambda message: message.text == "🧑‍🏫 Ментор")
def btn_mentor(message):
    bot.send_message(message.chat.id, data["mentor"])

@bot.message_handler(func=lambda message: message.text == "📈 Прогресс")
def btn_progress(message):
    bot.send_message(message.chat.id, data["progress"])

@bot.message_handler(func=lambda message: message.text == "🎮 Хобби")
def btn_hobby(message):
    bot.send_message(message.chat.id, data["hobby"])

@bot.message_handler(func=lambda message: message.text == "💼 Работы")
def btn_works(message):
    bot.send_message(message.chat.id, data["works"])

@bot.message_handler(func=lambda message: message.text == "🌐 GitHub")
def btn_github(message):
    bot.send_message(message.chat.id, data["github"])

@bot.message_handler(func=lambda message: message.text == "🎵 Мой TikTok")
def tiktok(message):
    bot.send_message(
        message.chat.id,
        "Мой TikTok: https://www.tiktok.com/@fan.gumball6?is_from_webapp=1&sender_device=pc"
    )

@bot.message_handler(func=lambda message: message.text == "💰 ИИ Бизнесмен")
def businessman(message):
    bot.send_message(
        message.chat.id,
        "💰 Напиши свой возраст, бюджет и что тебе интересно.\n\nПример:\n15 лет, 10000 тенге, TikTok"
    )

@bot.message_handler(func=lambda message: message.text == "🎧 Найти музыку")
def find_music(message):
    bot.send_message(
        message.chat.id,
        "🎧 Напиши название песни или исполнителя."
    )

@bot.message_handler(func=lambda message: message.text == "🎵 Мои любимые песни")
def send_music(message):
    music_folder = "music"

    files = [
        file for file in os.listdir(music_folder)
        if file.lower().endswith((".mp3", ".wav", ".ogg"))
    ]

    if not files:
        bot.send_message(message.chat.id, "❌ В папке music нет песен.")
        return

    for song in files:
        path = os.path.join(music_folder, song)

        with open(path, "rb") as audio:
            bot.send_audio(message.chat.id, audio)

@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    try:
        response = model.generate_content(message.text)

        if hasattr(response, "text"):
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Не удалось получить ответ.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка Gemini: {e}")

print("Бот запущен...")

bot.infinity_polling()