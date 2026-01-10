from sqlalchemy import Column, String, DateTime, Boolean
from app.models import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_candidate = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    ethereum_address = Column(String, nullable=True)
    role = Column(String, default="voter")  # voter, candidate, admin
    created_at = Column(DateTime, default=__import__('datetime').datetime.utcnow)
    updated_at = Column(DateTime, default=__import__('datetime').datetime.utcnow, onupdate=__import__('datetime').datetime.utcnow)
