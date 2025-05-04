from telegram import (
    Update,
    InlineKeyboardButton,
    KeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
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
from config.settings import logger
from config.states import States
from constants.enums.tables import TableName as tn
from constants.strings.format import SL
from constants.strings.partidas import *
from utils.formater import *
from datetime import datetime
from schemas import aventura


def new_button(text: str, callback_name: str) -> InlineKeyboardButton:
    """Helper function to create a button."""
    return InlineKeyboardButton(text, callback_data=callback_name)


def plazas_disponibles(aventura):
    plazas_totales = int(aventura["plazas_totales"])
    plazas_ocupadas = int(aventura["plazas_ocupadas"])
    plazas_sin_reserva = int(aventura["plazas_sin_reserva"])
    return plazas_totales - plazas_ocupadas - plazas_sin_reserva


async def lista(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    keyboard = []
    await query.edit_message_text(text=CARGANDO_LISTA)
    logger.info(CARGANDO_LISTA)
    try:
        sesiones = ses.get_partidas(details=True, soon=True)
        if sesiones:
            for sesion in sesiones:
                aventura = sesion[tn.AVENTURA]
                premisa = aventura[tn.PREMISA]
                title = f"{premisa['titulo']}, {premisa['sistema']}\n"
                keyboard.append([new_button(title, f"partida_detalle_{sesion['id']}")])
                logger.info(f"Created button: partida_detalle_{sesion['id']}")
            await query.edit_message_text(
                PROXIMAS,
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await query.message.edit_message_text(ZERO_RESULTS)
    except Exception as e:
        await query.message.reply_text(f"{ERROR_LISTA}: {e}")


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
    text += "Día y hora: " + fecha.strftime("%d/%m %H:%M")
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


async def partida_detalle(update: Update, partida_id: int):
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
            [new_button("Apuntarse", States.PARTIDA_UNIRSE.text)],
            [new_button("Volver a la lista", States.PARTIDA_LISTA.text)],
        ]
        await query.message.reply_text(
            "¿Quieres apuntarte?",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        await query.message.reply_text(f"{ERROR_DETALLES}: {e}")


async def pregunta_bool(pregunta: str, update: Update) -> None:
    """Pregunta al usuario respuesta booleana."""
    keyboard = [
        [InlineKeyboardButton("Sí"), InlineKeyboardButton("No")],
    ]
    await update.message.reply_text(
        pregunta, reply_markup=InlineKeyboardMarkup(keyboard)
    )


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
            new_button("No", "dirigir_titulo"),
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
