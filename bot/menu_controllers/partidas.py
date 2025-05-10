from telegram import Update
from telegram.ext import CallbackContext
from config.states import States
from handlers.partida import *
from menu_controllers.basic_options import desconocido


async def lista(update: Update, context: CallbackContext) -> int:
    # Detalles de partidas y volver?
    query = update.callback_query
    match query.data:
        case States.PARTIDA_DETALLES.name:
            return await partida_detalle(update, CallbackContext)
        case _:
            return await desconocido(update, context)


async def detalles(update: Update, context: CallbackContext) -> int:
    # Apuntarse o volver a lista
    query = update.callback_query
    match query.data:
        case States.PARTIDA_UNIRSE.name:
            return await partida_unirse(update, CallbackContext)
        case States.PARTIDA_LISTA.name:
            return await partida_lista(update, CallbackContext)
        case _:
            return await desconocido(update, context)
