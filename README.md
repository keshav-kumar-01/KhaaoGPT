# KhaoGPT 🍛

**Taste Intelligence · Food Discovery · Community Listings · Direct Ordering**

> Delhi has 50,000 restaurants. You've been eating from the same 20. KhaoGPT finds the other 49,980 that match exactly how your mouth works — including the street stall around the corner that no app has ever listed.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py               # runs at http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev                  # runs at http://localhost:5173
```

### Demo Login
- **Email:** admin@khaogpt.com
- **Password:** admin123

## Architecture
- **Backend:** Python + FastAPI + SQLAlchemy + SQLite
- **Frontend:** React + Vite + Tailwind CSS
- **Auth:** JWT tokens
- **Database:** SQLite for dev, PostgreSQL for production

## Features
- 🧬 **Taste DNA** — 5-question quiz mapping your palate across 7 axes
- 💬 **Chat** — Natural language food requests with personalised recommendations
- 👅 **First Bite** — Know how a dish will taste before ordering
- 💰 **True Cost** — Real price including delivery + platform fees
- 📍 **Community** — Users submit local spots with taste tags
- ⚙️ **Admin** — Approve/reject community submissions
- 🔗 **Order Redirect** — One tap to Zomato, Swiggy, or Google Maps

## Delhi NCR Launch Areas
Malviya Nagar · Hauz Khas · Saket · Connaught Place · Old Delhi · Cyber City · Sector 29 · Greater Kailash · Lajpat Nagar
