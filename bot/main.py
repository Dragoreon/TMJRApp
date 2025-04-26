from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from services import partidas as ses
from services import aventuras as ave
import logging
import os
from dotenv import load_dotenv
from utils.formater import *

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SL = "\n"  # Separador de líneas

# logger = logging.getLogger(__name__)
logging.basicConfig(filename="logs/tgbot.log", level=logging.INFO)

# Define states
MAIN_MENU, PARTIDA_LISTA, PARTIDA_DETALLES, PARTIDA_CREAR = range(4)


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


def new_button(text: str, callback_name: str) -> InlineKeyboardButton:
    """Helper function to create a button."""
    return InlineKeyboardButton(text, callback_data=callback_name)


async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "partida_lista":
        await partida_lista(update, query)
    elif query.data == "partida_anunciar":
        await query.edit_message_text(text="Quieres anunciar una partida")
        return PARTIDA_CREAR
    elif query.data.startswith("partida_detalle"):
        partida_id = query.data.split("_")[2]
        logging.info(f"Detalles de la partida: {partida_id}")
        await query.edit_message_text(text="Cargando detalles de la partida...")
        await partida_detalle(update, query, partida_id)
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


def plazas_disponibles(aventura):
    plazas_totales = int(aventura["plazas_totales"])
    plazas_ocupadas = int(aventura["plazas_ocupadas"])
    plazas_sin_reserva = int(aventura["plazas_sin_reserva"])
    return plazas_totales - plazas_ocupadas - plazas_sin_reserva


async def partida_lista(update: Update, query: CallbackQuery):
    keyboard = []
    await query.edit_message_text(text="Cargando partidas...")
    logging.info("Cargando partidas...")
    try:
        sesiones = ses.get_partidas(details=True, soon=True)
        if sesiones:
            for sesion in sesiones:
                aventura = sesion["Aventura"]
                premisa = aventura["Premisa"]
                title = f"{premisa['titulo']}, {premisa['sistema']}\n"
                keyboard.append([new_button(title, f"partida_detalle_{sesion['id']}")])
            await query.edit_message_text(
                "Estas son las próximas partidas",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await query.message.edit_message_text("No hay partidas disponibles :(")
    except Exception as e:
        await query.message.reply_text(f"Error al obtener partidas: {e}")


def partida_descripcion(sesion) -> str:
    """Genera la descripción de la partida."""
    aventura = sesion["Aventura"]
    premisa = aventura["Premisa"]
    num_sesiones = len(aventura["Sesion"])
    text = bold(premisa["titulo"]) + SL
    if premisa["sistema"]:
        text += "Sistema: " + premisa["sistema"] + SL
    text += aventura["lugar"] + SL
    if aventura["abierta_inscripcion"]:
        text += f"{plazas_disponibles(aventura)} plazas disponibles" + SL
    else:
        text += "*Inscripciones cerradas*" + SL
    if num_sesiones > 1:
        text += f"{num_sesiones} sesiones" + SL
    else:
        text += "Sesión única" + SL
    if premisa["descripcion"]:
        text += premisa["descripcion"] + SL
    return text


async def partida_detalle(update: Update, query: CallbackQuery, partida_id: int):
    try:
        sesion = ses.get_partida(partida_id, details=True)[0]
        logging.info(f"Sesión: {sesion}")
        if not sesion:
            await query.message.reply_text("No se encontró la partida")
            return
        descripcion = partida_descripcion(sesion)
        await query.edit_message_text(descripcion, parse_mode="HTML")
        # botones para apuntarse o volver a la lista
        keyboard = [
            [new_button("Apuntarse", f"apuntarse_{sesion['id']}_{query.from_user.id}")],
            [new_button("Volver a la lista", "partida_lista")],
        ]
        await query.message.reply_text(
            "¿Quieres apuntarte?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        await query.message.reply_text(f"Error al obtener detalles de la partida: {e}")


if __name__ == "__main__":
    main()
