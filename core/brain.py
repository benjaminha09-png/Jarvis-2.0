from google import genai


class Brain:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-3.6-flash"
        self.previous_interaction_id = None

    def think(self, message):
        try:
            if self.previous_interaction_id:
                interaction = self.client.interactions.create(
                    model=self.model,
                    input=message,
                    previous_interaction_id=self.previous_interaction_id,
                )
            else:
                interaction = self.client.interactions.create(
                    model=self.model,
                    input=message,
                )

            self.previous_interaction_id = interaction.id

            return interaction.output_text

        except Exception as error:
            error_text = str(error)

            if "429" in error_text or "quota" in error_text.lower():
                return (
                    "He alcanzado temporalmente el límite de solicitudes "
                    "de mi núcleo de inteligencia. Intenta de nuevo más tarde."
                )

            return f"Encontré un problema en mi núcleo: {error_text}"
