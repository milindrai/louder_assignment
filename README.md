# AI Event Concierge Platform

An AI-powered corporate event planning platform that takes natural language descriptions and returns structured venue proposals.

**Stack:** Django REST Framework · React.js (Vite) · MongoDB · Google Gemini / OpenAI

---

## Features

- 🤖 **AI-Powered Venue Proposals** — Describe your event in natural language, get structured suggestions
- 💾 **Persistent History** — All searches saved to MongoDB, visible on page refresh
- 🔄 **Dual LLM Support** — Works with either Gemini or OpenAI (auto-detects from API keys)
- 🎨 **Modern Dark UI** — Glassmorphism design with smooth animations

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB running locally (or a MongoDB Atlas connection string)
- A Gemini API key **or** OpenAI API key

### 1. Clone & Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your API key(s) and MongoDB URI
```

### 2. Start Backend

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

Backend runs at `http://localhost:8000`

### 3. Setup & Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | One of these | — | Google Gemini API key |
| `OPENAI_API_KEY` | must be set | — | OpenAI API key |
| `MONGODB_URI` | No | `mongodb://localhost:27017` | MongoDB connection string |
| `DJANGO_SECRET_KEY` | No | Auto-generated | Django secret key |
| `DEBUG` | No | `True` | Debug mode |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated hosts |
| `CORS_ALLOWED_ORIGINS` | No | `http://localhost:5173` | Comma-separated origins |

### Frontend

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | No | `http://localhost:8000/api` | Backend API URL |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/events/` | Submit an event description for AI processing |
| `GET`  | `/api/events/` | Retrieve all past searches (newest first) |

### POST Example

```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{"description": "A 10-person leadership retreat in the mountains for 3 days with a $4k budget"}'
```

---

## Deployment

### Frontend → Vercel

1. Push to GitHub
2. Import repo on [vercel.com](https://vercel.com)
3. Set **Root Directory** to `frontend`
4. Add env var: `VITE_API_URL` = your backend URL (e.g. `https://your-api.railway.app/api`)

### Backend → Railway / Render

1. Set **Root Directory** to `backend`
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `gunicorn concierge.wsgi --bind 0.0.0.0:$PORT`
4. Add env vars: `GEMINI_API_KEY`, `MONGODB_URI`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`

### Database → MongoDB Atlas

1. Create a free M0 cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Copy connection string → set as `MONGODB_URI` in backend env vars

---

## Project Structure

```
├── backend/
│   ├── concierge/          # Django project config
│   │   ├── settings.py     # Config (env-based)
│   │   ├── urls.py         # Root URL routing
│   │   └── wsgi.py
│   ├── events/             # Main app
│   │   ├── db.py           # MongoDB connection
│   │   ├── services.py     # AI service (Gemini/OpenAI)
│   │   ├── views.py        # REST API views
│   │   └── urls.py         # App routes
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main application
│   │   ├── index.css       # Design system
│   │   ├── api/client.js   # API client
│   │   └── components/     # UI components
│   └── package.json
└── README.md
```
