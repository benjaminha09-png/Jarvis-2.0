from google import genai


class Brain:
    def __init__(self):
        self.client = genai.Client()

        self.models = [
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash",
        ]

        self.previous_interaction_id = None

    def think(self, message):
        for model in self.models:
            try:
                if self.previous_interaction_id:
                    interaction = self.client.interactions.create(
                        model=model,
                        input=message,
                        previous_interaction_id=self.previous_interaction_id,
                    )
                else:
                    interaction = self.client.interactions.create(
                        model=model,
                        input=message,
                    )

                self.previous_interaction_id = interaction.id

                return interaction.output_text

            except Exception as error:
                error_text = str(error)

                if "429" in error_text or "quota" in error_text.lower():
                    continue

                return f"Encontré un problema en mi núcleo: {error_text}"

        return (
            "He alcanzado temporalmente el límite de mis modelos de inteligencia. "
            "Mi núcleo sigue funcionando, pero necesito esperar a que se restablezca la cuota."
        )
