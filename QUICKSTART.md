# 🚀 Quick Start Guide - SupaCall

Step-by-step guide to set up your AI phone system in 15 minutes.

## ⏱️ Estimated time: 15 minutes

---

## Step 1: Installation (2 min)

```bash
# Navigate to the folder
cd supacall

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: OpenAI Configuration (3 min)

### Get your API key:

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign in or create an account
3. Go to **API Keys** (left menu)
4. Click **Create new secret key**
5. Copy the key (starts with `sk-...`)

### Verify Realtime API access:

- The Realtime API requires an account with credit
- Check at [platform.openai.com/settings/organization/billing](https://platform.openai.com/settings/organization/billing)
- Add credit if needed (€5-10 is enough for testing)

---

## Step 3: Twilio Configuration (5 min)

### Create an account:

1. Go to [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up (free, €15 credit offered)
3. Verify your email and phone number

### Get a phone number:

1. In the Twilio dashboard, go to **Phone Numbers** → **Manage** → **Buy a number**
2. Choose your country (France: +33)
3. Check **Voice**
4. Click **Search** then **Buy** on a number
5. Copy your number (format: +33XXXXXXXXX)

### Retrieve your credentials:

1. In the dashboard, click **Account** → **Keys & Credentials**
2. Copy:
   - **Account SID** (starts with `AC...`)
   - **Auth Token** (click "Show")

---

## Step 4: Configure .env (2 min)

```bash
# Copy the template
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

Fill in:

```env
# Twilio (copy from dashboard)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+33123456789

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Server (leave localhost for now)
BASE_URL=http://localhost:8000

# Restaurant (customize)
RESTAURANT_NAME=Pizza 42
```

---

## Step 5: Test the configuration (1 min)

```bash
python test_system.py
```

If everything is OK, you will see ✅ everywhere!

---

## Step 6: Expose the server (2 min)

### Option A: Local development with ngrok

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from ngrok.com

# Terminal 1: Start the server
python main.py

# Terminal 2: Expose with ngrok
ngrok http 8000
```

Copy the ngrok URL (e.g. `https://abc123.ngrok.io`)

Update `.env`:
```env
BASE_URL=https://abc123.ngrok.io
```

Restart the server.

### Option B: Production deployment

See [README.md](README.md) for Railway, Render, etc.

---

## Step 7: Configure the Twilio webhook (2 min)

1. Go to [console.twilio.com](https://console.twilio.com/)
2. **Phone Numbers** → **Manage** → **Active numbers**
3. Click on your number
4. **Voice Configuration** section:
   - **Configure with**: Webhooks
   - **A call comes in**:
     - Webhook: `https://your-url.ngrok.io/incoming-call`
     - HTTP: POST
5. Click **Save**

---

## Step 8: TEST! 🎉

1. Call your Twilio number from your phone
2. The AI should answer and guide you through making a reservation
3. Check reservations: `http://localhost:8000/reservations`

---

## 🎯 Final checklist

- [ ] Python and dependencies installed
- [ ] Valid OpenAI API key with credit
- [ ] Twilio account with phone number
- [ ] .env file configured
- [ ] Configuration test passed (✅)
- [ ] Server started and exposed (ngrok)
- [ ] Twilio webhook configured
- [ ] Test call successful!

---

## ❌ Common issues

### "Could not resolve OpenAI API"
→ Check your API key and OpenAI credit

### "Webhook unreachable"
→ Check that ngrok is running and the URL is correct in Twilio

### "No audio"
→ Make sure your BASE_URL uses https, not http

### "Twilio error 11200"
→ Check that your server is publicly accessible

---

## 📚 Next steps

Once everything is working:

1. **Customize** the AI's voice and instructions ([main.py](main.py))
2. **Modify** opening hours and capacity (`.env`)
3. **Deploy** to production (Railway, Render, etc.)
4. **Add** features (SMS confirmation, calendar integration, etc.)

---

## 💡 Tips

- **Test locally first** with ngrok before deploying
- **Monitor costs** on OpenAI (~€0.30/min per call)
- **Back up** your database regularly
- **HTTPS is required** in production

---

Need help? Check the full [README.md](README.md)!
