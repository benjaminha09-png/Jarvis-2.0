from google import genai


class Brain:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.5-flash"

    def think(self, message):
        response = self.client.models.generate_content(
            model=self.model,
            contents=message
        )

        return response.text
