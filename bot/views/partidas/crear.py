from config.states import States
from constants.enums.tables import TableName as tn
from constants.strings.format import SL
from constants.strings.partidas import CREAR_INICIO
from constants.strings.basic import SI, NO, NO_DISPONIBLE
from config.settings import logger
from config.states import States
from utils.formater import *
from datetime import datetime
from handlers.basic_operations import new_button
from schemas.aventura import plazas_disponibles
from telegram import CallbackQuery
from telegram import (
    InlineKeyboardMarkup,
)


async def crear_inicio(query: CallbackQuery):
    keyboard = [
        [
            new_button(f"{SI} {NO_DISPONIBLE}", States.PARTIDA_CREAR_PREMISA.value),
            new_button(NO, States.PARTIDA_CREAR_TITULO.value),
        ],
    ]
    await query.edit_message_text(
        text=CREAR_INICIO,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
