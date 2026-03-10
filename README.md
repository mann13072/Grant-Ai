# Grant-Agent AI Prototype

## Run locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open:
- `http://localhost:8000/`
- `http://localhost:8000/index.html`
- Health check: `http://localhost:8000/health`

## Why this fixes "Not Found"

Some environments launch ASGI apps using `main:app` from the repository root. This repo now includes a root `main.py` that forwards to `app.main`, and supports both `/` and `/index.html` routes.
