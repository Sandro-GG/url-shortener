from database import get_db, engine, Base
from fastapi import FastAPI, Depends, HTTPException
from models import URL
from utils import encode
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from sqlalchemy import select

class URLRequest(BaseModel):
    target_url: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
app = FastAPI(lifespan=lifespan)


@app.post("/shorten")
async def shorten_url(payload: URLRequest, db: AsyncSession = Depends(get_db)):
    target = payload.target_url.strip()
    if not target.startswith(("http://", "https://")):
        target = f"https://{target}"
        
    new_entry = URL(original_url=target)
    
    db.add(new_entry)
    await db.flush()
    short_code = encode(new_entry.id)
    
    new_entry.short_code = short_code
    await db.commit()
    await db.refresh(new_entry)
    
    return {"short_url": f"http://localhost:8000/{short_code}"}


@app.get("/stats/{short_code}")
async def get_url_stats(short_code: str, db: AsyncSession = Depends(get_db)):
    query = select(URL).where(URL.short_code == short_code)
    result = await db.execute(query)
    url_entry = result.scalar_one_or_none()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short link not found")
    
    return {
        "short_code": url_entry.short_code,
        "original_url": url_entry.original_url,
        "clicks": url_entry.clicks,
        "created_at": url_entry.created_at
    }



@app.get("/{short_code}")
async def redirect_to_url(short_code: str, db: AsyncSession = Depends(get_db)):
    query = select(URL).where(URL.short_code == short_code)
    result = await db.execute(query)
    url_entry = result.scalar_one_or_none()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short link not found")
    
    url_entry.clicks += 1
    await db.commit()
    
    return RedirectResponse(url=url_entry.original_url)