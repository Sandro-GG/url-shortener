from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import sqlalchemy as sa

class URL(Base):
    __tablename__ = "urls"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column()
    short_code: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    clicks: Mapped[int] = mapped_column(default=0)
    