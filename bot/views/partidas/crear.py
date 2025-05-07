from config.states import States
from constants.strings.partidas import CREAR_INICIO, DIRIGIDO_LISTA
from constants.strings.basic import SI, NO, NO_DISPONIBLE
from config.states import States
from utils.formater import *
from handlers.basic_operations import new_button
from telegram import CallbackQuery
from telegram import (
    InlineKeyboardMarkup,
)


async def crear_inicio(query: CallbackQuery):
    keyboard = [
        [
            new_button(f"{SI} {NO_DISPONIBLE}", States.DIRIGIR_PREMISA_LISTA.value),
            new_button(NO, States.DIRIGIR_TITULO.value),
        ],
    ]
    await query.edit_message_text(
        text=CREAR_INICIO,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def crear_premisa_lista(query: CallbackQuery, premisas):
    keyboard = [[new_button(title, States.PARTIDA_DETALLES.name)] for title in premisas]
    await query.edit_message_text(
        text=DIRIGIDO_LISTA,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
