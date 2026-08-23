from brain import Brain


class Jarvis:
    def __init__(self):
        self.name = "JARVIS"
        self.version = "2.0"
        self.brain = Brain()

    def respond(self, message):
        return self.brain.think(message)


if __name__ == "__main__":
    jarvis = Jarvis()

    print("================================")
    print("       JARVIS 2.0 ONLINE")
    print("================================")
    print("Escribe 'salir' para apagarlo.\n")

    while True:
        message = input("Tú: ")

        if message.lower() in ["salir", "exit", "quit"]:
            print("JARVIS: Apagando sistemas.")
            break

        response = jarvis.respond(message)
        print(f"JARVIS: {response}")
