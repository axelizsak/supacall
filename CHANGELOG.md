# 📋 Changelog - SupaCall

History of changes and updates to the system.

---

## [1.1.0] - 2026-01-25

### ✅ Updated
- **Migration to `gpt-realtime`**: Switched from `gpt-4o-realtime-preview-2024-12-17` (deprecated on February 27, 2026) to the new production model `gpt-realtime`

### 🎯 Advantages of the new model
- **Stable production** version (not preview)
- Better handling of complex instructions
- More accurate function calling
- More natural and expressive voice
- **Image** input support
- Better interruption handling
- WebSocket, WebRTC and SIP support

### 📝 Available options
Two models to choose from:
- **`gpt-realtime`**: Recommended for best quality
- **`gpt-realtime-mini`**: Economical version for high volume

---

## [1.0.0] - 2026-01-25

### 🎉 Initial Release
- AI phone system for restaurant reservations
- Twilio + OpenAI Realtime API integration
- SQLite database for reservations
- REST API to view reservations
- Bidirectional WebSocket for real-time audio
- Automatic reservation management with availability checking
- Complete documentation (README, QUICKSTART, CUSTOMIZATION)
- Utility scripts (test_system.py, view_reservations.py)

### 🔧 Features
- Ultra-realistic voice with latency <500ms
- Natural interruptions handled
- 6 voices to choose from
- Customizable system instructions
- Functions: create reservation, check availability

---

## Planned Features

- [ ] Automatic confirmation SMS
- [ ] Google Calendar integration
- [ ] Reservation cancellation/modification
- [ ] Web dashboard for managing reservations
- [ ] Multi-language support
- [ ] POS system integration
- [ ] Detailed analytics and metrics
