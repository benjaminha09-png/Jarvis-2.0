from google import genai


class Brain:
    def __init__(self):
        self.client = genai.Client()

    def think(self, message):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )
        return response.text
