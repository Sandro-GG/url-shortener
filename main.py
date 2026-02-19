from database import get_db, engine, Base
from fastapi import FastAPI, Depends
from models import URL
from utils import encode
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager

class URLRequest(BaseModel):
    target_url: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/shorten")
async def shorten_url(payload: URLRequest, db: AsyncSession = Depends(get_db)):
    new_entry = URL(original_url=payload.target_url)
    
    db.add(new_entry)
    await db.flush()
    
    short_code = encode(new_entry.id)
    
    new_entry.short_code = short_code
    await db.commit()
    await db.refresh(new_entry)
    
    return {"short_url": f"http://localhost:8000/{short_code}"}
