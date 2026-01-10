from sqlalchemy import Column, String, DateTime, Integer, Text
from app.models import Base
from datetime import datetime
import uuid

class EmailJob(Base):
    __tablename__ = "email_jobs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    to_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, sent, failed
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
