# FitBuddy – AI Fitness Plan Generator (FastAPI + Gemini)

## Setup (VS Code terminal, Windows)
```
python -m venv fitbuddy-env
fitbuddy-env\Scripts\activate
pip install -r requirements.txt
```
(macOS/Linux: `source fitbuddy-env/bin/activate`)

## Add your Gemini API key
1. Get a key from https://aistudio.google.com/apikey
2. Copy `.env.example` to `.env` and replace `your_api_key_here`.
3. If Google reports that a model name is no longer available, check
   https://ai.google.dev/gemini-api/docs/models for current names and
   update `GEMINI_PRO_MODEL` / `GEMINI_FLASH_MODEL` in `.env`.

This project uses Google's `google-genai` package, which talks to the
Gemini API over plain HTTPS. It does not use `grpc`, so it avoids the
"Application Control policy has blocked this file" / `cygrpc` error
some Windows machines raise against the older `google-generativeai`
package.

## Run
```
uvicorn app.main:app --reload
```
- App:       http://127.0.0.1:8000
- API docs:  http://127.0.0.1:8000/docs
- Admin:     http://127.0.0.1:8000/view-all-users

## Optional
Put a gym photo at `static/images/gym-bg.jpg` for the background
(a gradient is used if the file is missing).
`fitbuddy.db` (SQLite) is created automatically on first run.
