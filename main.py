"""
AI phone system for restaurant reservations.
Uses Twilio + OpenAI Realtime API for an ultra-realistic experience.
"""
import asyncio
import json
import os
import websockets
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.responses import Response, HTMLResponse
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream

from database import db

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    await db.init_db()
    print(f"🚀 {os.getenv('RESTAURANT_NAME', 'Pizza 42')} - Reservation system started")
    yield
    # Shutdown
    print("👋 System shutting down")


app = FastAPI(
    title="SupaCall - AI Restaurant Reservations",
    lifespan=lifespan
)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RESTAURANT_NAME = os.getenv("RESTAURANT_NAME", "Pizza 42")
BASE_URL = os.getenv("BASE_URL", "https://your-domain.com")

# System instructions for the AI
SYSTEM_INSTRUCTIONS = f"""Tu es l'assistant téléphonique du restaurant {RESTAURANT_NAME}.

Ton rôle est de gérer les appels entrants et de prendre les réservations de manière professionnelle et chaleureuse.

PERSONNALITÉ:
- Tu es sympathique, professionnel(le) et efficace
- Tu parles français de manière naturelle avec un ton chaleureux
- Tu poses des questions de clarification si nécessaire
- Tu confirmes toujours les informations importantes

PROCESSUS DE RÉSERVATION:
1. Saluer l'appelant chaleureusement
2. Demander le nom complet
3. Demander la date souhaitée
4. Demander l'heure souhaitée
5. Demander le nombre de personnes
6. Demander un numéro de téléphone pour confirmer
7. Demander s'il y a des demandes spéciales ou allergies
8. Vérifier la disponibilité
9. Confirmer la réservation en résumant tous les détails

RÈGLES:
- Le restaurant est ouvert du mardi au samedi
- Heures de service: 11h30-14h30 (déjeuner) et 18h30-22h30 (dîner)
- Capacité maximale: 50 personnes
- Si c'est complet, propose d'autres horaires proches
- Sois naturel dans la conversation, pas robotique
- Gère les interruptions avec grâce
- Si l'appelant veut annuler ou modifier une réservation, note ses coordonnées et dis qu'un responsable le rappellera

IMPORTANT:
- Utilise la fonction create_reservation UNIQUEMENT quand tu as TOUTES les informations nécessaires
- Confirme verbalement la réservation après l'avoir créée
- Parle de manière naturelle, comme un vrai humain au téléphone
"""


@app.get("/")
async def root():
    """Home page"""
    return HTMLResponse(f"""
    <html>
        <head>
            <title>{RESTAURANT_NAME} - SupaCall</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{ margin-top: 0; }}
                .status {{
                    background: rgba(255,255,255,0.2);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📞 {RESTAURANT_NAME} - SupaCall</h1>
                <div class="status">
                    <h2>✅ System operational</h2>
                    <p>The AI phone system is online and ready to take reservations.</p>
                </div>
                <h3>Twilio Configuration:</h3>
                <p>Webhook for incoming calls: <code>{BASE_URL}/incoming-call</code></p>
                <p>WebSocket stream: <code>wss://{{domain}}/media-stream</code></p>
            </div>
        </body>
    </html>
    """)


@app.post("/incoming-call")
async def handle_incoming_call():
    """
    Endpoint called by Twilio when a call comes in.
    Returns TwiML to establish a WebSocket stream.
    """
    print("📞 Incoming call received")

    response = VoiceResponse()

    # Optional greeting message (can be handled by OpenAI instead)
    # response.say(
    #     f"Hello, you have reached {RESTAURANT_NAME}.",
    #     language="fr-FR",
    #     voice="Polly.Lea"
    # )

    # Establish a WebSocket stream connection
    connect = Connect()
    stream = Stream(url=f'wss://{BASE_URL.replace("https://", "").replace("http://", "")}/media-stream')
    connect.append(stream)
    response.append(connect)

    return Response(content=str(response), media_type="application/xml")


@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """
    WebSocket endpoint for handling the bidirectional audio stream
    between Twilio and the OpenAI Realtime API.
    """
    print("🔌 WebSocket connection established with Twilio")
    await websocket.accept()

    # Connect to OpenAI Realtime API
    openai_ws = None
    stream_sid = None

    try:
        # Connect to OpenAI Realtime API
        openai_ws = await websockets.connect(
            'wss://api.openai.com/v1/realtime?model=gpt-realtime',
            extra_headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "OpenAI-Beta": "realtime=v1"
            }
        )
        print("✅ Connected to OpenAI Realtime API (gpt-realtime)")

        # Configure the OpenAI session
        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": "alloy",
                "instructions": SYSTEM_INSTRUCTIONS,
                "modalities": ["text", "audio"],
                "temperature": 0.8,
                "tools": [
                    {
                        "type": "function",
                        "name": "create_reservation",
                        "description": "Creates a reservation in the system. Use ONLY when all information has been confirmed.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "nom": {
                                    "type": "string",
                                    "description": "Full name of the customer"
                                },
                                "telephone": {
                                    "type": "string",
                                    "description": "Customer phone number"
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Reservation date in YYYY-MM-DD format"
                                },
                                "heure": {
                                    "type": "string",
                                    "description": "Reservation time in HH:MM format"
                                },
                                "nombre_personnes": {
                                    "type": "integer",
                                    "description": "Number of guests"
                                },
                                "commentaires": {
                                    "type": "string",
                                    "description": "Comments or special requests"
                                }
                            },
                            "required": ["nom", "telephone", "date", "heure", "nombre_personnes"]
                        }
                    },
                    {
                        "type": "function",
                        "name": "check_availability",
                        "description": "Checks availability for a given date, time, and number of guests",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "description": "Date in YYYY-MM-DD format"
                                },
                                "heure": {
                                    "type": "string",
                                    "description": "Time in HH:MM format"
                                },
                                "nombre_personnes": {
                                    "type": "integer",
                                    "description": "Number of guests"
                                }
                            },
                            "required": ["date", "heure", "nombre_personnes"]
                        }
                    }
                ]
            }
        }
        await openai_ws.send(json.dumps(session_update))

        # Create tasks to handle messages in both directions
        async def receive_from_twilio():
            """Receives audio from Twilio and forwards it to OpenAI"""
            nonlocal stream_sid
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)

                    if data['event'] == 'start':
                        stream_sid = data['start']['streamSid']
                        print(f"📡 Stream started: {stream_sid}")

                    elif data['event'] == 'media':
                        # Audio from Twilio → OpenAI
                        audio_append = {
                            "type": "input_audio_buffer.append",
                            "audio": data['media']['payload']
                        }
                        await openai_ws.send(json.dumps(audio_append))

                    elif data['event'] == 'stop':
                        print("📡 Stream stopped")
                        break
            except Exception as e:
                print(f"❌ Error in receive_from_twilio: {e}")

        async def receive_from_openai():
            """Receives responses from OpenAI and forwards them to Twilio"""
            try:
                async for message in openai_ws:
                    response = json.loads(message)

                    # Handle different response types
                    if response['type'] == 'response.audio.delta':
                        # Audio from OpenAI → Twilio
                        audio_payload = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "payload": response['delta']
                            }
                        }
                        await websocket.send_json(audio_payload)

                    elif response['type'] == 'response.function_call_arguments.done':
                        # The AI wants to call a function
                        call_id = response['call_id']
                        function_name = response['name']
                        arguments = json.loads(response['arguments'])

                        print(f"🔧 Function call: {function_name}")
                        print(f"   Arguments: {arguments}")

                        # Execute the function
                        result = await execute_function(function_name, arguments)

                        # Return the result to OpenAI
                        function_output = {
                            "type": "conversation.item.create",
                            "item": {
                                "type": "function_call_output",
                                "call_id": call_id,
                                "output": json.dumps(result, ensure_ascii=False)
                            }
                        }
                        await openai_ws.send(json.dumps(function_output))

                        # Request a response
                        await openai_ws.send(json.dumps({"type": "response.create"}))

                    elif response['type'] == 'error':
                        print(f"❌ OpenAI error: {response}")

            except Exception as e:
                print(f"❌ Error in receive_from_openai: {e}")

        # Run both tasks in parallel
        await asyncio.gather(
            receive_from_twilio(),
            receive_from_openai()
        )

    except Exception as e:
        print(f"❌ WebSocket error: {e}")

    finally:
        if openai_ws:
            await openai_ws.close()
        print("🔌 WebSocket connection closed")


async def execute_function(function_name: str, arguments: dict) -> dict:
    """Executes a function called by the AI"""
    try:
        if function_name == "create_reservation":
            # Create the reservation in the database
            reservation = await db.create_reservation(
                nom=arguments['nom'],
                telephone=arguments['telephone'],
                date=arguments['date'],
                heure=arguments['heure'],
                nombre_personnes=arguments['nombre_personnes'],
                commentaires=arguments.get('commentaires', '')
            )
            print(f"✅ Reservation created: {reservation}")
            return {
                "success": True,
                "reservation_id": reservation['id'],
                "message": f"Reservation confirmed for {arguments['nom']} on {arguments['date']} at {arguments['heure']} for {arguments['nombre_personnes']} guest(s)."
            }

        elif function_name == "check_availability":
            # Check availability
            available = await db.check_availability(
                date=arguments['date'],
                heure=arguments['heure'],
                nombre_personnes=arguments['nombre_personnes']
            )
            return {
                "available": available,
                "message": "Available" if available else "Fully booked at this time"
            }

        else:
            return {"error": f"Unknown function: {function_name}"}

    except Exception as e:
        print(f"❌ Error executing {function_name}: {e}")
        return {"error": str(e)}


@app.get("/reservations")
async def get_reservations():
    """Endpoint to view all reservations"""
    reservations = await db.get_all_reservations()
    return {"reservations": reservations}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", 8000)),
        reload=True
    )
