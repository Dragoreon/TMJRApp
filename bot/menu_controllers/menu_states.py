from config.states import States
from telegram.ext import CallbackQueryHandler
from views.start import start
from menu_controllers.main_menu import main_menu
from menu_controllers.partidas import lista, detalles

# Todos los estados que puede tener el bot y sus métodos controladores que manejan las respuestas
MENU_STATES = {
    States.MAIN_MENU.value: [CallbackQueryHandler(main_menu)],
    States.PARTIDA_LISTA.value: [CallbackQueryHandler(lista)],
    States.PARTIDA_DETALLES.value: [CallbackQueryHandler(detalles)],
    # States.PARTIDA_CREAR: [CallbackQueryHandler(crear)],
}
