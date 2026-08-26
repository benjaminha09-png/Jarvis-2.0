from brain import Brain


class Jarvis:
    def __init__(self):
        self.name = "JARVIS"
        self.version = "2.0"
        self.brain = Brain()
        self.active = False

    def activate(self):
        self.active = True
        return "Buen día, Benja. ¿En qué puedo ayudarte?"

    def respond(self, message):
        return self.brain.think(message)


if __name__ == "__main__":
    jarvis = Jarvis()

    print("================================")
    print("       JARVIS 2.0 ONLINE")
    print("================================")
    print("Escribe 'Jarvis' o 'Hola Jarvis' para activarme.")
    print()

    while True:
        message = input("Tú: ").strip()
        command = message.lower()

        # Apagar completamente JARVIS
        if command in ["salir", "exit", "quit"]:
            print("JARVIS: Apagando sistemas.")
            break

        # Desactivar JARVIS
        if command in ["adios jarvis", "adiós jarvis", "bye jarvis"]:
            if jarvis.active:
                jarvis.active = False
                print("JARVIS: Hasta luego, Benja.")
            else:
                print("JARVIS: Ya estoy en modo de espera.")
            continue

        # Activar JARVIS
        if not jarvis.active:
            if command in ["jarvis", "hola jarvis"]:
                print(f"JARVIS: {jarvis.activate()}")
            continue

        # JARVIS está activo y puede responder
        response = jarvis.respond(message)
        print(f"JARVIS: {response}")
