import os
from dotenv import load_dotenv
import telebot
import routers.sesiones as ses
import models.sesion as Sesion

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['ini'])
def send_welcome(message):
    bot.send_message(message.chat.id, "¡Hola! ¿Qué deseas hacer?\nVer partidas: /partidas")

@bot.message_handler(commands=['partidas'])
def partidas(message):
    bot.send_message(message.chat.id, "Aquí tienes la lista de partidas:")
    partidas = ses.get_partidas()
    if not partidas:
        bot.send_message(message.chat.id, "No hay partidas disponibles.")
        return
    for partida in partidas:
        bot.send_message(message.chat.id, f"Nombre: {partida.titulo}")

print("Bot is running...")
bot.infinity_polling()