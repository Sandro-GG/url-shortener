# URL Shortener API

A lightweight, asynchronous URL shortening service built with **FastAPI** and **PostgreSQL**.

## Features
- **Deterministic Shortening:** Uses Base62 encoding on database IDs to ensure unique, short slugs.
- **Async Backend:** Fully non-blocking database operations using SQLAlchemy 2.0.
- **Click Tracking:** Built-in analytics to monitor link usage.
- **Auto-Normalization:** Handles missing protocols (adds `https://` automatically).

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

2. **Database:**
   - Create a PostgreSQL database named `url-shortener`.
   - Update the connection string in `database.py` with your credentials:
     `postgresql+asyncpg://user:password@localhost:5432/url-shortener`

3. **Run the Application:**
   ```bash
   uvicorn main:app --reload

## API Endpoints
- `POST /shorten` - Submit a long URL; returns a short link.
- `GET /{short_code}` - Redirects to the destination and increments click count.
- `GET /stats/{short_code}` - Returns JSON data (Original URL, clicks, timestamp).

## Test
1. **Shorten:** Use Swagger UI at `http://127.0.0.1:8000/docs` to POST a URL.
2. **Redirect:** Visit the generated short link in your browser.
3. **Verify:** Check the `/stats/{short_code}` endpoint to see the click count increase.