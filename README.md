# AI Lead Hunter
**Maintained by: Muhammad Irfan**

AI-powered Google Maps lead generation. 100% free stack — no paid APIs.

---

## Stack
| Layer | Tech |
|-------|------|
| Backend | Python FastAPI + SQLAlchemy |
| Database | PostgreSQL |
| Scraper | Playwright (headless Chromium) |
| AI | Ollama (Mistral local) |
| Frontend | HTML + Bootstrap Icons + Vanilla JS |
| Deploy | Railway (backend) + Netlify (frontend) |

---

## Local Development

### Option A — Docker (recommended)
```bash
# 1. Start DB + Backend
docker-compose up -d

# 2. Install Ollama + pull model
# https://ollama.com/download
ollama pull mistral

# 3. Serve frontend
cd frontend && python -m http.server 3000
# Open: http://localhost:3000/login.html
```

### Option B — Manual
```bash
# 1. Create DB
createdb leadhunter

# 2. Backend
cd backend
cp .env.example .env      # fill in DATABASE_URL + SECRET_KEY
pip install -r requirements.txt
playwright install chromium
python main.py            # runs on http://localhost:8000

# 3. Ollama AI
ollama pull mistral && ollama serve

# 4. Frontend
cd frontend
python -m http.server 3000
```

---

## Deploy to Production

### Backend → Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select the `backend/` folder (it auto-detects the Dockerfile)
4. Add a PostgreSQL plugin in Railway
5. Set environment variables:

```
DATABASE_URL    → (Railway auto-fills from plugin)
SECRET_KEY      → any random 32-char string
OLLAMA_BASE_URL → your Ollama server URL (or leave for Railway hosted)
OLLAMA_MODEL    → mistral
DEBUG           → False
```

6. Copy the Railway public URL (e.g. `https://ai-lead-hunter.up.railway.app`)

### Frontend → Netlify

1. Go to [netlify.com](https://netlify.com) → New site → Import from GitHub
2. Set **Publish directory** to `frontend`
3. Edit `frontend/config.js`:
```js
const APP_CONFIG = {
  API_BASE: 'https://ai-lead-hunter.up.railway.app'  // your Railway URL
};
```
4. Deploy — Netlify gives you a free `.netlify.app` domain

### Auto Deploy (GitHub Actions)

Add these secrets in GitHub → Settings → Secrets:
```
RAILWAY_TOKEN       → from Railway account settings
NETLIFY_AUTH_TOKEN  → from Netlify user settings
NETLIFY_SITE_ID     → from Netlify site settings
```

Every push to `main` auto-deploys both frontend and backend.

---

## API Reference
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | No | Register |
| POST | `/api/auth/login` | No | Login → JWT |
| POST | `/api/search` | Yes | Scrape + analyze |
| GET | `/api/leads/{id}` | Yes | Get leads |
| GET | `/api/export/{id}?format=csv` | Yes | Export |
| GET | `/api/dashboard/stats` | Yes | Stats |
| GET | `/health` | No | Health check |

---

## Folder Structure
```
ai-lead-hunter/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── Dockerfile
│   ├── railway.toml
│   ├── requirements.txt
│   ├── models/          # User, Search, Lead
│   ├── routes/          # auth, search, dashboard
│   ├── controllers/     # business logic
│   ├── middleware/      # JWT auth
│   └── services/
│       ├── scraper/     # Playwright Maps scraper
│       └── ai/          # Ollama lead analyzer
├── frontend/
│   ├── config.js        # API_BASE URL config
│   ├── login.html
│   ├── register.html
│   ├── index.html       # Dashboard
│   ├── search.html      # Search form
│   ├── leads.html       # Leads table + export
│   ├── netlify.toml
│   ├── components/sidebar.html
│   └── assets/
│       ├── css/app.css
│       └── js/api.js | utils.js | layout.js
├── docker-compose.yml
├── .gitignore
└── .github/workflows/deploy.yml
```
