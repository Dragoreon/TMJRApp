from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from services import partidas as ses
from services import aventuras as ave
import logging
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/tgbot.log', level=logging.INFO)

# Define states
MAIN_MENU, PARTIDA_LISTA, PARTIDA_DETALLES = range(3)

async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Ver próximas partidas", callback_data="partida_lista")],
        [InlineKeyboardButton("Anunciar partida", callback_data="partida_anunciar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "¡Hola! Elige una opción", reply_markup=reply_markup
    )
    return MAIN_MENU

async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "partida_lista":
        await partida_lista(update, query)
    elif query.data == "partida_anunciar":
        await query.edit_message_text(text="Quieres anunciar una partida")
        return PARTIDA_DETALLES
    else:
        await query.edit_message_text(text="Opción desconocida")
        return MAIN_MENU


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .read_timeout(10)
        .write_timeout(10)
        .concurrent_updates(True)
        .build()
    )

    # ConversationHandler to handle the state machine
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("inicio", start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(button)],
            PARTIDA_LISTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
            PARTIDA_DETALLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
        },
        fallbacks=[CommandHandler("inicio", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()
    application.idle()

async def partida_lista(update: Update, query: CallbackQuery):
    await query.edit_message_text(text="Estas son las próximas partidas")
    # Get list of partidas / sesiones
    try:
        sesiones = ses.get_partidas_week(details=True)
    except Exception as e:
        await query.message.reply_text(f"Error al obtener partidas: {e}")
        start(query.message, None)
    if sesiones:
        partida_text = ''
        for sesion in sesiones:
            logging.info(sesion)
            aventura = sesion['Aventura']
            premisa = aventura['Premisa']
            partida_text += f"{premisa['titulo']}, {premisa['sistema']}\n"
        await query.message.reply_text(partida_text)
        # back to main menu button0
    else:
        await query.message.reply_text("No hay partidas disponibles :(")

    return PARTIDA_LISTA

if __name__ == "__main__":
    main()
