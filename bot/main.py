from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
)
from config.settings import TOKEN
from menu_controllers.menu_states import MENU_STATES
from views.start import start


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
        states=MENU_STATES,
        fallbacks=[CommandHandler("inicio", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()
    application.idle()


if __name__ == "__main__":
    main()
