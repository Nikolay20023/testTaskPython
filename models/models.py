from sqlalchemy import Column, String, ForeignKey
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
import uuid


from models.base import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.UUID)
    username: str = Column(String(length=128), unique=True, nullable=False)
    hashed_password = Column(String())
    
    weathers: Mapped[List["Weather"]] = relationship(back_populates="user")


class Weather(Base):
    __tablename__ = "weathers"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.UUID)
    city: str = Column(String())
    data: str = Column(String())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="weathers")