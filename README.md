# High-Performance URL Shortener

A modern, asynchronous URL shortening API built with **FastAPI** and **PostgreSQL**. This project demonstrates a full-stack backend architecture including database transactions, mathematical encoding algorithms, and RESTful API design.

## Key Features
- **Base62 Encoding:** Converts auto-incrementing database IDs into compact, URL-friendly short codes.
- **Asynchronous Architecture:** Uses `SQLAlchemy 2.0` (Async) and `asyncpg` for non-blocking database operations.
- **Data Normalization:** Automatically handles URL protocols (http/https) to ensure redirect integrity.
- **Real-time Analytics:** Tracks click counts per URL with a dedicated stats endpoint.
- **Automatic Documentation:** Interactive API exploration via Swagger UI.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0 (Async)
- **Validation:** Pydantic v2
- **Server:** Uvicorn

## System Design & Logic
This shortener avoids random string collisions by using a **Base62 Bijective Mapping** strategy. 
1. The system accepts a long URL and creates a record in PostgreSQL.
2. The unique `BigInt` ID of that record is encoded into Base62 (0-9, a-z, A-Z).
3. This ensures every short link is unique, deterministic, and as short as mathematically possible.

## Setup & Installation
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/url-shortener.git](https://github.com/YOUR_USERNAME/url-shortener.git)
   cd url-shortener

2. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Database Configuration:**
   - Ensure **PostgreSQL** is installed and running.
   - Create a database named `url-shortener`.
   - Update the connection string in `database.py` with your credentials:
     `postgresql+asyncpg://user:password@localhost:5432/url-shortener`

5. **Run the Application:**
   ```bash
   uvicorn main:app --reload

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/shorten` | **Ingestion:** Accepts a JSON payload with a `target_url`. Validates/normalizes the URL and returns a Base62 encoded short link. |
| `GET` | `/{short_code}` | **Resolution:** Lookups the code in PostgreSQL, increments the click counter, and performs a `307 Temporary Redirect` to the original URL. |
| `GET` | `/stats/{short_code}` | **Analytics:** Returns a JSON object containing the original URL, total clicks, and the creation timestamp. |

## Testing the Flow

To verify the full system functionality, follow these steps:

1. **Access Documentation:**
   Navigate to `http://127.0.0.1:8000/docs` to use the built-in Swagger UI.

2. **Generate a Link:**
   Use the **POST** `/shorten` endpoint with a body like:
   ```json
   { "target_url": "google.com" }
   *Note: The API will automatically prepend `https://` if it is missing to ensure valid redirection.*

3. **Trigger Redirect:**
   Copy the `short_url` from the response (e.g., `http://localhost:8000/1`) and paste it into your browser address bar.

4. **Verify Analytics:**
   Visit `http://localhost:8000/stats/1`. You should see the `clicks` count has incremented to reflect your visit.

---
## Security Features
As a project focused on robust backend design, the following measures are implemented:
- **SQL Injection Prevention:** Utilizes SQLAlchemy's expression language to ensure all queries are parameterized.
- **Input Sanitization:** Uses Pydantic for schema validation and custom logic to normalize inbound URLs.
- **Error Handling:** Implements clear HTTP exception states (404, 422, 500) to avoid exposing stack traces.