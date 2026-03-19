# Event Concierge Platform

A full-stack corporate event planning application that takes natural language descriptions and returns structured, intelligent venue proposals. 

**Stack:** Django REST Framework, React.js (Vite), MongoDB, Google Gemini / OpenAI / Groq

---

## Features

- **Natural Language Parsing:** Describe your event requirements natively and receive structured, specific venue suggestions.
- **Data Persistence:** All searches are saved to MongoDB asynchronously and persist across sessions.
- **Provider Fallback Layer:** Built-in adapter that automatically handles API rate-limits by seamlessly falling back through available LLM providers (Gemini → OpenAI → Groq).
- **Graceful Degradation:** Includes a local heuristic engine to ensure the platform remains functional even if all external APIs are exhausted.
- **Modern UI:** Responsive, accessible interface built with React and Tailwind concepts.

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
| `GEMINI_API_KEY` | At least one | — | Google Gemini API key |
| `OPENAI_API_KEY` | provider | — | OpenAI API key |
| `GROQ_API_KEY`   | required | — | Groq API key (Recommended fallback) |
| `MONGODB_URI` | No | `mongodb://localhost:27017` | MongoDB connection string |
| `DJANGO_SECRET_KEY` | No | Auto-generated | Django secret key |
| `DEBUG` | No | `True` | Debug mode |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated hosts |
| `CORS_ALLOWED_ORIGINS`| No | `http://localhost:5173` | Comma-separated origins |
| `CORS_ALLOW_ALL`  | No | `False` | Helpful flag for deployment |

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

### Backend (Render)

1. Connect your repository to [Render](https://render.com) and create a **Web Service**.
2. **Root Directory:** `backend`
3. **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. **Start Command:** `gunicorn concierge.wsgi --bind 0.0.0.0:$PORT`
5. Add env vars: `GROQ_API_KEY`, `MONGODB_URI`, `DEBUG=False`

### Frontend (Render Static Site / Vercel)

1. Connect repo to create a **Static Site** (Render) or **Project** (Vercel).
2. **Root Directory:** `frontend`
3. **Build Command:** `npm run build`
4. **Publish Directory:** `dist`
5. Add env var: `VITE_API_URL` = your deployed backend API URL (e.g., `https://my-backend.onrender.com/api`)

### Database (MongoDB Atlas)

1. Create a free M0 cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Obtain connection string and set as `MONGODB_URI` in the backend environment.

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
