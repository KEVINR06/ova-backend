import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔑 API KEY DESDE RENDER
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 📚 CONTENIDO POR LECCIÓN
contenidos = {

    "leccion1": """
Tema: Introducción a la informática
- Hardware: partes físicas del computador
- Software: programas y aplicaciones
- Ejemplos: teclado, Word, Windows
""",

    "leccion2": """
Tema: Circuitos eléctricos
- Circuito en serie
- Circuito en paralelo
- LED
- Resistencia
- Batería
- Conductores
""",

    "leccion3": """
Tema: Arduino y programación por bloques
- Sensores
- LEDs
- Bloques condicionales
- Automatización
""",

    "leccion4": """
Tema: Algoritmos y diagramas de flujo
- void setup()
- void loop()
- Diagramas
- Decisiones
"""
}

@app.route("/chat", methods=["POST"])
def chat():

    try:

        # 📩 DATOS RECIBIDOS
        data = request.json

        mensaje = data.get("mensaje", "").lower()
        leccion = data.get("leccion", "leccion1")

        # 📚 CONTENIDO SEGÚN LECCIÓN
        contenido = contenidos.get(leccion, "")

        # 🧠 PROMPT EDUCATIVO MÁS NATURAL
        prompt = f"""
Eres un tutor virtual de informática para estudiantes de grado 8.

OBJETIVO:
Ayudar al estudiante a comprender la lección actual de manera amigable, educativa y conversacional.

REGLAS:
- Responde SOLO temas relacionados con la lección actual
- Mantén una conversación natural
- Puedes responder preguntas relacionadas indirectamente
- Guía paso a paso
- No entregues respuestas completas de evaluaciones
- Usa ejemplos sencillos
- Explica de forma clara y corta
- Máximo 6 líneas

Si el estudiante pregunta algo MUY fuera del tema:
redirige amablemente la conversación hacia la lección.

CONTENIDO DE LA LECCIÓN:
{contenido}

PREGUNTA DEL ESTUDIANTE:
{mensaje}
"""

        # 🔐 HEADERS
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # 🚀 PETICIÓN A GROQ
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={

                "model": "llama-3.1-8b-instant",

                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                "temperature": 0.5,
                "max_tokens": 180
            }
        )

        # 📥 RESPUESTA
        result = response.json()

        print("RESPUESTA GROQ:", result)

        # 🚨 SI HAY ERROR
        if "choices" not in result:

            return jsonify({
                "respuesta": "❌ Error en Groq"
            })

        # 🤖 RESPUESTA FINAL
        respuesta = result["choices"][0]["message"]["content"]

        return jsonify({
            "respuesta": respuesta.strip()
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "respuesta": "❌ Error del servidor"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)