class State:
    def __init__(self, number, text):
        self.value = {"num": number, "text": text}

    @property
    def num(self):
        return self.value["num"]

    @property
    def text(self):
        return self.value["text"]


class States:
    MAIN_MENU = State(1, "main_menu")
    PARTIDA_LISTA = State(2, "partida_lista")
    PARTIDA_DETALLES = State(3, "partida_detalles")
    PARTIDA_CREAR = State(4, "partida_crear")
    PARTIDA_UNIRSE = State(5, "partida_unirse")
