# SupaCall - AI Phone System for Restaurant Reservations

An ultra-realistic AI phone system using **Twilio** + **OpenAI Realtime API** to automatically handle restaurant reservations for **Pizza 42**.

##  Features

-  **Ultra-realistic voice** with OpenAI Realtime API
-  **Ultra-low latency** (<500ms)
-  **Natural interruptions** handled automatically
-  **Full reservation management** (creation, availability check)
-  **SQLite database** to store reservations
-  **REST API** to view reservations
-  **Simple configuration** via .env file

##  Installation

### 1. Prerequisites

- Python 3.9+
- Twilio account (free for testing)
- OpenAI API key with Realtime API access
- Publicly accessible server (ngrok for dev, or a production server)

### 2. Install dependencies

```bash
# Clone or navigate to the project folder
cd supacall

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+33123456789

# OpenAI Configuration
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
BASE_URL=https://your-domain.com

# Restaurant Configuration
RESTAURANT_NAME=Pizza 42
RESTAURANT_OPENING_HOURS=11:30-14:30,18:30-22:30
RESTAURANT_MAX_CAPACITY=50
```

##  Twilio Configuration

### 1. Create a Twilio account

1. Go to [twilio.com](https://www.twilio.com/)
2. Sign up (free for testing)
3. Get a phone number

### 2. Configure the webhook

In the Twilio console:

1. Go to **Phone Numbers** → **Manage** → **Active numbers**
2. Click on your number
3. In the **Voice Configuration** section:
   - **A call comes in**: Webhook → `https://your-domain.com/incoming-call` → HTTP POST

### 3. Get your credentials

- **Account SID**: In the Twilio Dashboard
- **Auth Token**: In the Twilio Dashboard (click "Show")

##  OpenAI Configuration

### 1. Get an API key

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Create an API key
3. Make sure you have access to the Realtime API (may require a paid account)

### 2. Verify access

The Realtime API uses the `gpt-4o-realtime-preview-2024-12-17` model.

##  Deployment

### Option 1: Local development with ngrok

To test locally:

```bash
# Terminal 1: Start the server
python main.py

# Terminal 2: Expose with ngrok
ngrok http 8000
```

Copy the ngrok URL (e.g. `https://abc123.ngrok.io`) and use it as `BASE_URL` in Twilio.

### Option 2: Production (Railway, Render, etc.)

#### Example with Railway:

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Deploy:
```bash
railway login
railway init
railway up
```

3. Configure environment variables in the Railway dashboard

#### Example with Render:

1. Create an account on [render.com](https://render.com)
2. Create a new **Web Service**
3. Connect your GitHub repo
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
5. Add environment variables

##  Usage

### Start the server

```bash
python main.py
```

The server starts at `http://0.0.0.0:8000`

### Test the system

1. **Call the configured Twilio number**
2. The AI will answer automatically and guide the caller
3. Reservations are saved to the database

### View reservations

Via the API:
```bash
curl http://localhost:8000/reservations
```

Or open in the browser: `http://localhost:8000/reservations`

##  API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page / status |
| `/incoming-call` | POST | Twilio webhook (called automatically) |
| `/media-stream` | WebSocket | Bidirectional audio stream |
| `/reservations` | GET | List all reservations |

##  Customization

### Choose the Realtime API model

The system currently uses **`gpt-realtime`** (stable production version). You can change the model in [main.py](main.py):

**Available options:**

```python
# Option 1: gpt-realtime (RECOMMENDED - production version)
'wss://api.openai.com/v1/realtime?model=gpt-realtime'

# Option 2: gpt-realtime-mini (ECONOMICAL - cheaper)
'wss://api.openai.com/v1/realtime?model=gpt-realtime-mini'
```

**Comparison:**
- **gpt-realtime**: Best quality, complex instructions, image support
- **gpt-realtime-mini**: More economical, good for high volume, still performant

### Modify the AI personality

Edit the `SYSTEM_INSTRUCTIONS` variable in [main.py](main.py):

```python
SYSTEM_INSTRUCTIONS = f"""Tu es l'assistant téléphonique du restaurant {RESTAURANT_NAME}.
...
"""
```

### Modify opening hours and capacity

In the `.env` file:

```env
RESTAURANT_OPENING_HOURS=11:30-14:30,18:30-22:30
RESTAURANT_MAX_CAPACITY=50
```

### Add custom functions

In [main.py](main.py), add new functions to the `tools` list:

```python
{
    "type": "function",
    "name": "cancel_reservation",
    "description": "Cancels a reservation",
    "parameters": {...}
}
```

And implement in `execute_function()`.

##  Troubleshooting

### Problem: AI does not respond

- Check that `BASE_URL` is correct in `.env`
- Check that the Twilio webhook points to `https://your-domain.com/incoming-call`
- Check server logs

### Problem: WebSocket connection error

- Check that your server supports WebSockets
- If using a proxy (nginx, etc.), configure correctly:

```nginx
location /media-stream {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Problem: Poor audio quality

- Check your internet connection
- The Realtime API requires a stable connection
- Try changing the voice in `session_update` (options: alloy, echo, fable, onyx, nova, shimmer)

##  Estimated costs

### Twilio
- Phone number: ~€1/month
- Incoming calls: ~€0.013/minute
- [Twilio pricing](https://www.twilio.com/pricing)

### OpenAI Realtime API
- Audio input: $0.06/minute
- Audio output: $0.24/minute
- Approximately €0.30/minute per call
- [OpenAI pricing](https://openai.com/pricing)

**Example**: For 100 calls averaging 3 minutes:
- Twilio: 100 × 3 × €0.013 = €3.90
- OpenAI: 100 × 3 × €0.30 = €90
- **Total: ~€94/month**

##  Security

- ✅ Never commit the `.env` file
- ✅ Use HTTPS in production
- ✅ Validate Twilio webhooks with their signature
- ✅ Restrict API access with authentication

##  Resources

- [Twilio Documentation](https://www.twilio.com/docs)
- [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

##  Support

For any questions or issues:
1. Check server logs
2. Consult Twilio and OpenAI documentation
3. Test locally with ngrok first

---

Built to automate restaurant reservations.
