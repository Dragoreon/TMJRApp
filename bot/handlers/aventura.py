from telegram import Update
from telegram.ext import CallbackContext
from config.settings import logger
from config.states import States
from constants.strings.partidas import *
from utils.formater import *
from views.partidas.crear import crear_inicio


async def dirigir_titulo(update: Update, context: CallbackContext) -> None:
    logger.info("Sacar título")
    query = update.callback_query
    # Recoger título
    # TODO: ni idea de cómo hacer esto
    # await query.edit_message_reply_markup(text="¿Título de la aventura?")
    # titulo = update.message.text
    # logger.info("Titulo " + titulo)
    # if not titulo:
    #     await query.message.reply_text("No has introducido un título")


async def dirigir_get_premisa(update: Update, context: CallbackContext) -> None:
    # Si ha dirigido antes, buscar en la base de datos
    query = update.callback_query
    logger.info("Get premisa")
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


async def dirigir_inicio(update: Update, context: CallbackContext) -> None:
    logger.info(f"{update.effective_user.username} quiere dirigir")
    # TODO: Empezar a guardar cosas en caché?
    await crear_inicio(update.callback_query)
    return States.DIRIGIR
