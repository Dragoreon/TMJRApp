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
from config.settings import logger, TOKEN
from utils.formater import *
from handlers.partida import *
from config.states import States
from views.view_controller import view


async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Ver próximas partidas", callback_data="lista")],
        [InlineKeyboardButton("Dirigir partida", callback_data="dirigir")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info("Iniciando bot")
    # logger.info("Usuario: %s", update.message.from_user.username)
    await update.message.reply_text(
        "¡Hola! Elige una opción", reply_markup=reply_markup
    )
    return States.MAIN_MENU.text


async def button(update: Update, context: CallbackContext) -> int:
    logger.info("Button clicked")
    logger.info("Button name: " + update.callback_query.data)
    return view(update, context)


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
            States.MAIN_MENU.num: [CallbackQueryHandler(button)],
            States.PARTIDA_LISTA.num: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)
            ],
            States.PARTIDA_DETALLES.num: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)
            ],
            States.PARTIDA_CREAR.num: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)
            ],
        },
        fallbacks=[CommandHandler("inicio", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()
    application.idle()


if __name__ == "__main__":
    main()
