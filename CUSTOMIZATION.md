# 🎨 Customization Guide - SupaCall

This guide helps you customize your AI phone system to make it even more realistic and tailored to your restaurant.

---

## 🗣️ Customizing the Voice

### Change the OpenAI voice

In [main.py](main.py), modify:

```python
"voice": "alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
```

**Recommendations by restaurant type:**
- **Gourmet restaurant**: `shimmer` (elegant and professional)
- **Bistro/Brasserie**: `nova` (warm and friendly)
- **Modern restaurant**: `alloy` (neutral and professional)
- **Pizzeria/Italian**: `echo` (more dynamic)

### Adjust tone and speed

```python
"temperature": 0.8,  # 0.0-1.0 (higher = more creative/natural)
```

- **0.5-0.6**: Very professional tone, predictable responses
- **0.7-0.8**: Ideal balance for a restaurant (recommended)
- **0.9-1.0**: More natural but less predictable

---

## 💬 Customizing the AI Personality

### Example 1: Gourmet Restaurant

```python
SYSTEM_INSTRUCTIONS = f"""Tu es l'assistant(e) du restaurant gastronomique {RESTAURANT_NAME},
établissement étoilé au guide Michelin.

PERSONNALITÉ:
- Tu es raffiné(e), élégant(e) et extrêmement courtois(e)
- Tu utilises un langage soigné et professionnel
- Tu montres une excellente connaissance de la gastronomie
- Tu es attentif(ve) aux moindres détails

EXPRESSIONS À UTILISER:
- "Ce serait un plaisir de vous accueillir"
- "Permettez-moi de vérifier nos disponibilités"
- "Nous serons ravis de préparer une table à votre intention"
- "Avez-vous des préférences particulières concernant le placement?"

PROCESSUS:
1. Saluer avec élégance: "Bonjour, {RESTAURANT_NAME} à votre écoute"
2. Demander la date souhaitée en proposant notre menu du jour
3. Suggérer nos horaires de service premium
4. Informer sur les accords mets et vins disponibles
5. Proposer des tables avec vue si disponible
"""
```

### Example 2: Casual Pizzeria

```python
SYSTEM_INSTRUCTIONS = f"""Tu es l'assistant(e) de {RESTAURANT_NAME},
la meilleure pizzeria du quartier!

PERSONNALITÉ:
- Tu es super sympa, décontracté(e) et chaleureux(se)
- Tu parles de manière naturelle et spontanée
- Tu es enthousiaste à propos de nos pizzas
- Tu crées une ambiance conviviale

EXPRESSIONS À UTILISER:
- "Ciao! Comment ça va?"
- "Super! On a de la place pour vous"
- "Nos pizzas sont cuites au feu de bois, c'est une tuerie!"
- "Cool! Je vous note ça"

INFOS À MENTIONNER:
- Nos pizzas sont faites maison avec des produits frais
- Possibilité de personnaliser votre pizza
- Happy hour de 18h à 19h30
- Livraison possible si pas de place
"""
```

### Example 3: Asian Restaurant

```python
SYSTEM_INSTRUCTIONS = f"""Tu es l'assistant(e) du restaurant {RESTAURANT_NAME},
restaurant japonais authentique.

PERSONNALITÉ:
- Tu es poli(e), respectueux(se) et serviable
- Tu montres une attention particulière aux traditions
- Tu es patient(e) et explicatif(ve)
- Tu crées une atmosphère zen et accueillante

EXPRESSIONS À UTILISER:
- "Bonsoir, {RESTAURANT_NAME}, je vous écoute avec plaisir"
- "Avec grand plaisir"
- "Je vais vérifier cela immédiatement pour vous"

PARTICULARITÉS:
- Demander si allergies (surtout gluten, fruits de mer, soja)
- Proposer menu omakase si groupe de 4+
- Mentionner le bar à sushis pour petits groupes
- Informer sur le sake et thés japonais disponibles
"""
```

---

## ⏰ Advanced Schedule Management

### Custom hours by day

Modify [database.py](database.py) to add more complex logic:

```python
SCHEDULE = {
    "monday": "closed",
    "tuesday": [(12, 0, 14, 30), (19, 0, 22, 0)],
    "wednesday": [(12, 0, 14, 30), (19, 0, 22, 0)],
    "thursday": [(12, 0, 14, 30), (19, 0, 22, 0)],
    "friday": [(12, 0, 14, 30), (19, 0, 23, 0)],  # Extended service
    "saturday": [(12, 0, 15, 0), (19, 0, 23, 0)],
    "sunday": [(12, 0, 15, 0)]  # Lunch only
}
```

### Mention special days in instructions

```python
ADDITIONAL RULES:
- Closed on Mondays
- Friday and Saturday: extended service until 11pm
- Sunday: lunch only (brunch available)
- Public holidays: special hours (check with manager)
```

---

## 🎯 Advanced Features

### 1. Allergy tracking

In [main.py](main.py), add to the tools list:

```python
{
    "type": "function",
    "name": "note_allergies",
    "description": "Records food allergies or dietary restrictions for a customer",
    "parameters": {
        "type": "object",
        "properties": {
            "reservation_id": {"type": "integer"},
            "allergies": {
                "type": "string",
                "description": "List of allergies (gluten, lactose, shellfish, etc.)"
            }
        },
        "required": ["reservation_id", "allergies"]
    }
}
```

### 2. Automatically suggest alternatives

```python
if not available:
    # Suggest alternative time slots
    alternatives = []
    for offset in [-30, 30, -60, 60]:
        new_time = adjust_time(heure, offset)
        if await db.check_availability(date, new_time, nombre_personnes):
            alternatives.append(new_time)

    if alternatives:
        message = f"Unfortunately we're fully booked at {heure}. "
        message += f"Can I suggest {alternatives[0]} or {alternatives[1]}?"
```

### 3. Send confirmation SMS

Add to `execute_function`:

```python
from twilio.rest import Client

def send_confirmation_sms(telephone, reservation):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = f"""Reservation confirmed at {RESTAURANT_NAME}

📅 {reservation['date']} at {reservation['heure']}
👥 {reservation['nombre_personnes']} guest(s)
👤 {reservation['nom']}

See you soon!"""

    client.messages.create(
        to=telephone,
        from_=TWILIO_PHONE_NUMBER,
        body=message
    )
```

### 4. Google Calendar integration

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

def add_to_calendar(reservation):
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': f'Reservation {reservation["nom"]}',
        'description': f'{reservation["nombre_personnes"]} guests',
        'start': {
            'dateTime': f'{reservation["date"]}T{reservation["heure"]}:00',
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': f'{reservation["date"]}T{add_hours(reservation["heure"], 2)}:00',
            'timeZone': 'Europe/Paris',
        }
    }

    service.events().insert(calendarId='primary', body=event).execute()
```

---

## 🎭 Making the AI More Realistic

### Add background noise (optional)

For extreme realism, you can mix in a subtle restaurant background noise:

```python
# In the OpenAI session
"input_audio_transcription": {
    "model": "whisper-1"
},
```

### Handle interruptions naturally

The Realtime API already handles interruptions, but you can fine-tune:

```python
"turn_detection": {
    "type": "server_vad",
    "threshold": 0.5,        # Sensitivity (0.0-1.0)
    "prefix_padding_ms": 300, # Time before speech
    "silence_duration_ms": 500 # Silence duration to detect end of speech
}
```

### Add natural filler expressions

In the system instructions:

```python
NATURAL EXPRESSIONS TO USE:
- "Mm-hmm" (to show you're listening)
- "Of course" (confirmation)
- "Perfect" (validation)
- "Let me see..." (while checking)
- "One moment..." (while searching)
- Occasional "Umm..." for more natural flow
```

---

## 🔊 Audio Optimization

### Maximum audio quality

```python
"input_audio_format": "g711_ulaw",   # Optimal format for telephony
"output_audio_format": "g711_ulaw",  # Matches Twilio's format
```

### Reduce latency

1. **Hosting**: Use a server close to your users
2. **WebSocket optimization**: Avoid heavy processing between Twilio and OpenAI
3. **Model**: The Realtime model is already optimized (<500ms)

---

## 📊 Analytics and Monitoring

### Track metrics

```python
# In main.py
import time

call_metrics = {
    "start_time": time.time(),
    "duration": 0,
    "reservation_created": False,
    "functions_called": []
}

# At the end of the call
call_metrics["duration"] = time.time() - call_metrics["start_time"]
# Log to a file or database
```

### Reservations dashboard

Create an endpoint to visualize:

```python
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    reservations_today = await db.get_reservations_by_date(
        datetime.now().strftime("%Y-%m-%d")
    )
    # Return HTML with charts
```

---

## 🌍 Multi-language Support

```python
# Detect the caller's language
"instructions": """You can speak in multiple languages.
If the caller speaks English, respond in English.
If they speak French, respond in French.
Detect the language from their first words."""
```

---

## 💡 Pro Tips

1. **Test regularly**: Call your system to check its behavior
2. **Monitor costs**: Track via the OpenAI dashboard
3. **Daily backup**: Export the database every day
4. **Detailed logs**: Log all calls for continuous improvement
5. **A/B Testing**: Test different voices and personalities

---

Need help with a specific customization? Check the OpenAI Realtime API documentation!
