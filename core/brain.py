from google import genai
import json
import os


class Brain:
    def __init__(self):
        self.client = genai.Client()

        self.models = [
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash",
        ]

        self.previous_interaction_id = None

        # Archivo de memoria
        self.memory_file = "../memory/memory.json"
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r", encoding="utf-8") as file:
                    return json.load(file)
        except Exception:
            pass

        return []

    def save_memory(self):
        try:
            with open(self.memory_file, "w", encoding="utf-8") as file:
                json.dump(self.memory, file, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def think(self, message):

        # Guardar recuerdos cuando Benja lo pide
        if message.lower().startswith("recuerda que"):
            memory = message[11:].strip()

            if memory:
                self.memory.append(memory)
                self.save_memory()

                return f"Entendido, Benja. Lo recordaré: {memory}"

        # Preparar los recuerdos para JARVIS
        memories = ""

        if self.memory:
            memories = "\n".join(
                f"- {memory}" for memory in self.memory
            )

        for model in self.models:
            try:

                prompt = f"""
Eres JARVIS, el asistente personal de Benja.

Tu personalidad:
- Inteligente y educado.
- Directo y natural.
- Siempre llamas al usuario "Benja".
- Nunca digas que eres Gemini, salvo que Benja te pregunte directamente.
- Cuando Benja salude al comenzar una conversación, responde exactamente:
  "Buen día, Benja. ¿En qué puedo ayudarte?"

Memoria de Benja:
{memories if memories else "No hay recuerdos guardados todavía."}

Mensaje de Benja:
{message}
"""

                if self.previous_interaction_id:
                    interaction = self.client.interactions.create(
                        model=model,
                        input=prompt,
                        previous_interaction_id=self.previous_interaction_id,
                    )
                else:
                    interaction = self.client.interactions.create(
                        model=model,
                        input=prompt,
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
