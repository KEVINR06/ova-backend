import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#  CONTENIDO POR LECCIÓN
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

#  PALABRAS VÁLIDAS
palabras_validas = [
    "hardware","software","informática",
    "circuito","led","resistencia","batería",
    "arduino","sensor","bloques",
    "algoritmo","setup","loop","diagrama"
]

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.json

        mensaje = data.get("mensaje", "").lower()
        leccion = data.get("leccion", "leccion1")

        contenido = contenidos.get(leccion, "")

        #  BLOQUEO FUERA DE TEMA
        if not any(p in mensaje for p in palabras_validas):

            return jsonify({
                "respuesta": "❌ Esa pregunta no pertenece a esta lección."
            })

        #  PROMPT EDUCATIVO
        prompt = f"""
Eres un tutor virtual de informática para estudiantes de grado 8.

REGLAS:
- SOLO responde usando la lección actual
- NO des respuestas completas
- Guía paso a paso
- Explicación corta y clara
- Máximo 5 líneas
- Si no pertenece al tema responde:
"Esa pregunta no pertenece a esta lección"

CONTENIDO:
{contenido}

PREGUNTA:
{mensaje}
"""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

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

                "temperature": 0.3,
                "max_tokens": 120
            }
        )

        #  RESPUESTA
        result = response.json()

        print("RESPUESTA GROQ:", result)

        #  SI HAY ERROR
        if "choices" not in result:
            return jsonify({
                "respuesta": "❌ Error en Groq"
            })

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