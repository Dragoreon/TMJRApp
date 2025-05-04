from config.settings import logger
from config.states import States as States
from handlers.partida import *


async def view(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    match query.data:
        case States.PARTIDA_LISTA.text:
            await lista(update, context)
            return States.PARTIDA_LISTA.num
        case States.PARTIDA_DETALLES.text:
            # TODO sacar el id de un archivo o caché redis
            # partida_id = data.split("_")[2]
            # logger.info(f"Detalles de la partida: {partida_id}")
            # await partida_detalle(update, partida_id)
            return States.PARTIDA_DETALLES.num
        case States.PARTIDA_CREAR.text:
            await dirigir(update, context)
            return States.PARTIDA_CREAR.num
        # case "dirigir_titulo":
        #     await dirigir_titulo(update, context)
        #     return States.PARTIDA_CREAR.num
        case _:
            await query.edit_message_text(text="Opción desconocida")
            return States.MAIN_MENU.num
