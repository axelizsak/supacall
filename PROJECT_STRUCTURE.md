# 📁 SupaCall Project Structure

```
supacall/
│
├── main.py                 # 🎯 Main FastAPI server + Twilio/OpenAI logic
├── database.py             # 💾 SQLite database management
├── requirements.txt        # 📦 Python dependencies
├── .env                    # 🔐 Environment variables (to create - never commit)
├── .env.example            # 📝 Configuration template
├── .gitignore              # 🚫 Files ignored by Git
│
├── README.md               # 📚 Full documentation
├── QUICKSTART.md           # 🚀 Quick start guide (15 min)
├── CUSTOMIZATION.md        # 🎨 Customization guide
├── PROJECT_STRUCTURE.md    # 📁 This file
│
├── test_system.py          # 🧪 Configuration tests
├── view_reservations.py    # 👀 Reservation viewer
├── start.sh                # ▶️  Quick start script
│
└── reservations.db         # 💾 Database (created automatically)
```

---

## 📄 File Descriptions

### Core Files

#### [main.py](main.py)
**The heart of the system** - FastAPI server that handles:
- 📞 Incoming Twilio calls
- 🔌 Bidirectional WebSocket between Twilio and OpenAI
- 🤖 AI configuration (voice, instructions, functions)
- 🎙️ Real-time audio streaming
- 📋 Function execution (create reservation, check availability)

**Key endpoints:**
- `GET /` - Home page and status
- `POST /incoming-call` - Twilio webhook (TwiML)
- `WebSocket /media-stream` - Audio stream
- `GET /reservations` - Reservations API

#### [database.py](database.py)
**Database management** - `ReservationDB` class for:
- ✅ Creating reservations
- 🔍 Checking availability
- 📊 Retrieving reservations by date
- 💾 Async SQLite storage

**Main functions:**
- `init_db()` - Initializes the DB
- `create_reservation()` - Creates a reservation
- `check_availability()` - Checks availability
- `get_reservations_by_date()` - Retrieves by date

---

### Configuration

#### [.env](/.env.example)
**Environment variables** (to create from `.env.example`):
```env
TWILIO_ACCOUNT_SID=         # Twilio Account SID
TWILIO_AUTH_TOKEN=          # Twilio Auth Token
TWILIO_PHONE_NUMBER=        # Your Twilio number
OPENAI_API_KEY=             # OpenAI API key
BASE_URL=                   # Public server URL
RESTAURANT_NAME=            # Your restaurant name
```

#### [requirements.txt](requirements.txt)
**Python dependencies:**
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `twilio` - Twilio SDK
- `openai` - OpenAI SDK
- `websockets` - WebSocket support
- `aiosqlite` - Async SQLite

---

### Documentation

#### [README.md](README.md)
**Full documentation:**
- ✨ Feature overview
- 🚀 Detailed installation
- 📋 Twilio and OpenAI configuration
- 🌐 Deployment options
- 🔧 Troubleshooting
- 💰 Cost estimation

#### [QUICKSTART.md](QUICKSTART.md)
**Quick guide (15 minutes):**
- ⏱️ Chronological steps
- 📝 Complete checklist
- 🎯 Focused on essentials
- ❌ Solutions to common issues

#### [CUSTOMIZATION.md](CUSTOMIZATION.md)
**Customization guide:**
- 🗣️ Change voice and tone
- 💬 Personality examples (gourmet, casual, etc.)
- ⏰ Advanced schedule management
- 🎯 Extra features (SMS, Google Calendar, etc.)
- 🎭 Tips for more realism

---

### Tools and Scripts

#### [test_system.py](test_system.py)
**Configuration tests** - Verifies:
- ✅ Environment variables
- ✅ API key validity
- ✅ Twilio configuration
- ✅ Database connection
- 📊 Summary with statistics

**Usage:**
```bash
python test_system.py
```

#### [view_reservations.py](view_reservations.py)
**Reservation viewer** - Displays:
- 📅 Reservations grouped by date
- 👥 Full details (name, phone, guests, etc.)
- 📊 Global statistics
- 🏆 Insights (largest reservation, averages, etc.)

**Usage:**
```bash
python view_reservations.py
```

#### [start.sh](start.sh)
**Quick start script:**
- Checks the virtual environment
- Activates the environment
- Checks the `.env` file
- Installs dependencies if needed
- Runs tests (optional)
- Starts the server

**Usage:**
```bash
./start.sh
```

---

### Database

#### reservations.db
**SQLite database** created automatically - Structure:

```sql
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    telephone TEXT NOT NULL,
    date TEXT NOT NULL,              -- Format: YYYY-MM-DD
    heure TEXT NOT NULL,             -- Format: HH:MM
    nombre_personnes INTEGER NOT NULL,
    commentaires TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'confirmed'
);
```

---

## 🔄 Data Flow

```
1. Incoming call
   └─> Twilio receives the call
       └─> POST /incoming-call (main.py)
           └─> Returns TwiML with WebSocket URL
               └─> WebSocket /media-stream established

2. Audio stream
   └─> Client audio → Twilio → WebSocket → OpenAI
       └─> OpenAI processes and responds
           └─> OpenAI audio → WebSocket → Twilio → Client

3. Function call (e.g. create_reservation)
   └─> OpenAI detects intent
       └─> Calls function via WebSocket
           └─> execute_function() (main.py)
               └─> database.py creates the reservation
                   └─> Result returned to OpenAI
                       └─> OpenAI verbally confirms to client
```

---

## 🎯 Extension Points

### Adding a new feature:

1. **Define the function** in `session_update` ([main.py](main.py))
2. **Implement** in `execute_function()` ([main.py](main.py))
3. **Test** with a real call
4. **Update** system instructions if needed

### Example features to add:

- ✉️ Automatic confirmation SMS
- 📅 Google Calendar integration
- ❌ Reservation cancellation
- 🔄 Reservation modification
- 📧 Confirmation email
- 💳 Pre-payment with Stripe
- 📊 Analytics dashboard
- 🌍 Multi-language support
- 📱 Push notifications

---

## 🔒 Security

**Sensitive files** (NEVER commit):
- `.env` - Contains API keys
- `reservations.db` - Customer data
- `*.log` - Logs that may contain sensitive info

**Already in .gitignore:**
```
.env
*.db
*.sqlite
*.log
__pycache__/
venv/
```

---

## 📊 Metrics to Monitor

In production, track:
- 📞 Number of calls/day
- ⏱️ Average call duration
- ✅ Reservation completion rate
- ❌ Call abandonment rate
- 💰 OpenAI and Twilio costs
- 🐛 Errors/exceptions

---

## 🚀 Possible Future Improvements

1. **Web Admin Interface** for managing reservations
2. **Calendar Integration** (Google Calendar, Outlook)
3. **Analytics Dashboard** with graphs
4. **Multi-restaurant** (manage multiple restaurants)
5. **Multilingual AI** (automatic language detection)
6. **Automatic reminders** (SMS 24h before)
7. **Waiting list** when fully booked
8. **POS Integration** (restaurant point-of-sale systems)

---

Need help? Check [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)!
