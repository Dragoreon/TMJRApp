from telegram import Update
from telegram.ext import CallbackContext
from config.states import States
from config.settings import logger
from handlers.partida import partida_lista
from handlers.aventura import dirigir_inicio
from views.start import start
from menu_controllers.basic_options import desconocido


async def main_menu(update: Update, context: CallbackContext) -> int:
    logger.info("Main menu controller")
    query = update.callback_query
    match query.data:
        case States.MAIN_MENU.name:
            return await start(update, context)
        case States.PARTIDA_LISTA.name:
            return await partida_lista(update, context)
        case States.PARTIDA_CREAR.name:
            return await dirigir_inicio(update, context)
        case _:
            return await desconocido(update, context)
