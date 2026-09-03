import json
import os
import re

from google import genai


class Brain:

    def __init__(self):

        # Conexión con Gemini
        self.client = genai.Client()

        # Modelos de respaldo
        self.models = [
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash",
        ]

        # Ruta correcta de la memoria
        self.memory_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "memory",
            "memory.json"
        )

        # Cargar memoria
        self.memory = self.load_memory()


    # ==========================================
    # CARGAR MEMORIA
    # ==========================================

    def load_memory(self):

        try:

            if os.path.exists(self.memory_file):

                with open(
                    self.memory_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    if isinstance(data, list):
                        return data

        except Exception:
            pass

        return []


    # ==========================================
    # GUARDAR MEMORIA
    # ==========================================

    def save_memory(self):

        try:

            os.makedirs(
                os.path.dirname(self.memory_file),
                exist_ok=True
            )

            with open(
                self.memory_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.memory,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as error:

            print(
                f"Error guardando memoria: {error}"
            )


    # ==========================================
    # RECORDAR INFORMACIÓN
    # ==========================================

    def remember(self, message):

        text = message.strip()

        patterns = [
            r"mi perro se llama (.+)",
            r"mi perra se llama (.+)",
            r"mi mascota se llama (.+)",
            r"mi color favorito es (.+)",
            r"mi comida favorita es (.+)",
            r"me gusta (.+)",
            r"recuerda que (.+)",
            r"recuerda (.+)",
            r"guarda que (.+)",
            r"guarda (.+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                information = match.group(1).strip()

                if information:

                    memory_text = text

                    # Evitar duplicados
                    if memory_text not in self.memory:

                        self.memory.append(memory_text)

                        self.save_memory()

                    return True, information

        return False, None


    # ==========================================
    # PENSAR
    # ==========================================

    def think(self, message):

        # Primero comprobar si Benja quiere guardar algo
        was_saved, information = self.remember(message)

        if was_saved:

            return (
                f"Entendido, Benja. "
                f"Lo recordaré: {information}."
            )


        # Preparar recuerdos
        if self.memory:

            memory_text = "\n".join(
                f"- {item}"
                for item in self.memory
            )

        else:

            memory_text = "No hay recuerdos guardados."


        # Instrucciones de JARVIS
        prompt = f"""
Eres JARVIS, el asistente personal de Benja.

PERSONALIDAD:
- Eres inteligente, educado y natural.
- Respondes de forma clara y directa.
- Siempre llamas al usuario "Benja".
- No digas que eres Gemini.
- No menciones que eres una inteligencia artificial de Google.
- Compórtate como JARVIS.
- Si no sabes algo, dilo claramente.
- No inventes recuerdos.

MEMORIA DE BENJA:
{memory_text}

INSTRUCCIONES SOBRE LA MEMORIA:
- Usa la memoria anterior para responder preguntas.
- Si Benja pregunta por algo que aparece en la memoria, úsalo.
- Si la información no aparece en la memoria, no afirmes que la recuerdas.
- No confundas información nueva con información guardada.

MENSAJE DE BENJA:
{message}

Responde de manera natural y breve.
"""


        # Probar los modelos disponibles
        for model in self.models:

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response and response.text:

                    return response.text.strip()

            except Exception as error:

                error_text = str(error)

                # Si es límite de cuota,
                # intentar el siguiente modelo
                if (
                    "429" in error_text
                    or "quota" in error_text.lower()
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    continue

                return (
                    "Encontré un problema en mi núcleo: "
                    f"{error_text}"
                )


        # Si todos los modelos están limitados
        return (
            "Benja, temporalmente alcancé el límite "
            "de mis modelos de inteligencia. "
            "Mi memoria local sigue funcionando."
        )
