from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext
from config.settings import logger
from config.states import States
from constants.enums.tables import TableName as tn
from constants.strings.format import SL
from constants.strings.partidas import *
from utils.formater import *
from datetime import datetime
from handlers.basic_operations import new_button


async def dirigir_titulo(update: Update, context: CallbackContext) -> None:
    logger.info("Sacar título")
    query = update.callback_query
    await query.answer()
    # Recoger título
    await query.edit_message_reply_markup(text="¿Título de la aventura?")
    titulo = update.message.text
    logger.info("Titulo " + titulo)
    if not titulo:
        await query.message.reply_text("No has introducido un título")


async def dirigir_get_premisa(update: Update, context: CallbackContext) -> None:
    # Si ha dirigido antes, buscar en la base de datos
    query = update.callback_query
    logger.info("Get premisa")
    await query.answer()
    await query.edit_message_text(text="Cargando aventuras dirigidas...")
    # try:
    #     premisas = ave.get_premisas_by_user(query.from_user.id)
    #     if premisas:
    #         keyboard = []
    #         for premisa in premisas:
    #             aventura = premisa["Premisa"]
    #             title = f"{premisa['titulo']}, {premisa['sistema']}\n"
    #             keyboard.append(
    #                 [new_button(title, f"partida_detalle_{aventura['id']}")]
    #             )
    #         await query.edit_message_text(
    #             "Estas son las aventuras que has dirigido",
    #             reply_markup=InlineKeyboardMarkup(keyboard),
    #         )
    #     else:
    #         await query.message.reply_text(
    #             "No he encontrado aventuras dirigidas por ti."
    #             + SL
    #             + "Vamos a crear una nueva."
    #         )
    #         # await titulo(update, context)
    # except Exception as e:
    #     await query.message.reply_text(f"Error al obtener aventuras: {e}")


async def dirigir(update: Update, context: CallbackContext) -> None:
    logger.info(f"{update.effective_user.username} quiere dirigir")
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            new_button("Sí (No disponible por ahora)", "dirigir_get_premisa"),
            new_button("No", States.PARTIDA_CREAR_TITULO.value),
        ],
    ]
    await query.edit_message_text(
        text="Tengo que saber algunas cosas antes de empezar."
        + SL
        + "¿Has dirigido antes esta aventura?"
        + SL
        + "(Si la has dirigido pero no la has registrado antes, responde 'no')",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
