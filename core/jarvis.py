class Jarvis:
    def __init__(self):
        self.name = "JARVIS"
        self.version = "2.0"

    def respond(self, message):
        return f"{self.name}: Recibí tu mensaje: {message}"


if __name__ == "__main__":
    jarvis = Jarvis()

    print("JARVIS 2.0 iniciado.")
    print("Escribe 'salir' para terminar.")

    while True:
        message = input("Tú: ")

        if message.lower() in ["salir", "exit", "quit"]:
            print("JARVIS: Hasta luego.")
            break

        print(jarvis.respond(message))
