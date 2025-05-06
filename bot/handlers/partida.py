from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext
from services import partidas as ses
from services import aventuras as ave
from config.settings import logger
from config.states import States
from constants.enums.tables import TableName as tn
from constants.strings.format import SL
from constants.strings.partidas import *
from utils.formater import *
from datetime import datetime
from schemas import aventura
from handlers.basic_operations import new_button
from schemas.aventura import plazas_disponibles


async def lista(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    keyboard = []
    await query.edit_message_text(text=CARGANDO_LISTA)
    logger.info(CARGANDO_LISTA)
    try:
        sesiones = ses.get_partidas(details=True, soon=True)
        if sesiones:
            for sesion in sesiones:
                aventura = sesion[tn.AVENTURA.value]
                premisa = aventura[tn.PREMISA.value]
                title = f"{premisa['titulo']}, {premisa['sistema']}"
                # Guardar sesion['id'] en caché
                keyboard.append([new_button(title, States.PARTIDA_DETALLES.name)])
                # logger.info(f"Created button: " + States.PARTIDA_DETALLES.name)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                PROXIMAS,
                reply_markup=reply_markup,
            )
        else:
            await query.edit_message_text(ZERO_RESULTS)
    except Exception as e:
        await query.message.reply_text(f"{ERROR_LISTA}: {e}")
    return States.PARTIDA_LISTA.value


def partida_descripcion(sesion) -> str:
    """Genera la descripción de la partida."""
    aventura = sesion["Aventura"]
    premisa = aventura["Premisa"]
    num_sesiones = len(aventura["Sesion"])
    text = bold(premisa["titulo"]) + SL
    if premisa["sistema"]:
        text += "Sistema: " + premisa["sistema"] + SL
    text += SL + "Lugar: " + aventura["lugar"] + SL
    fecha = datetime.strptime(sesion["fecha"], "%Y-%m-%dT%H:%M:%S")
    text += "Día y hora: " + fecha.strftime("%d/%m %H:%M") + SL
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


async def partida_detalle(update: Update, context: CallbackContext) -> int:
    partida_id = 1  # TODO: sacar esto de caché o algo así
    logger.info(f"Detalles de la partida: {partida_id}")
    query = update.callback_query
    await query.edit_message_text(text=CARGANDO_DETALLES)
    try:
        sesion = ses.get_partida(partida_id, details=True)[0]
        logger.info(f"Sesión id: {sesion['id']}")
        if not sesion:
            await query.message.reply_text(ZERO_RESULTS)
            return
        descripcion = partida_descripcion(sesion)
        await query.edit_message_text(descripcion, parse_mode="HTML")
        # botones para apuntarse o volver a la lista
        # TODO: guardar sesion['id'] en caché
        keyboard = [
            [new_button("Apuntarse", States.PARTIDA_UNIRSE.name)],
            [new_button("Volver a la lista", States.PARTIDA_LISTA.name)],
        ]
        logger.info(keyboard)
        await query.message.reply_text(
            "¿Quieres apuntarte?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        await query.message.reply_text(f"{ERROR_DETALLES}: {e}")
    return States.PARTIDA_DETALLES.value


async def partida_unirse(update: Update, context: CallbackContext) -> int:
    logger.info("Unirse a partida")
    return States.PARTIDA_UNIRSE.value
