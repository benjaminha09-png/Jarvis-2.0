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
    print("Di o escribe 'Hola JARVIS' o 'JARVIS' para activarme.")
    print()

    while True:
        message = input("Tú: ").strip()

        if message.lower() in ["salir", "exit", "quit"]:
            print("JARVIS: Apagando sistemas.")
            break

        # JARVIS está esperando la palabra de activación
        if not jarvis.active:
            if message.lower() in ["jarvis", "hola jarvis"]:
                print(f"JARVIS: {jarvis.activate()}")
            continue

        # Una vez activado, responde normalmente
        response = jarvis.respond(message)
        print(f"JARVIS: {response}")
