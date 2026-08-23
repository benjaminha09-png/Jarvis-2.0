class Brain:
    def __init__(self):
        self.name = "JARVIS"
        self.model = "free"

    def think(self, message):
        message = message.strip()

        if not message:
            return "No recibí ningún mensaje."

        if "hola" in message.lower():
            return "Hola. Estoy listo."

        if "quién eres" in message.lower() or "quien eres" in message.lower():
            return "Soy JARVIS, tu asistente personal."

        return f"Entendido: {message}"
