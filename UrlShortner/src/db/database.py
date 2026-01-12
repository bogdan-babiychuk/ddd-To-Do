from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass



class Url(Base):
    __tablename__ = "Url"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(String, unique=True)
    