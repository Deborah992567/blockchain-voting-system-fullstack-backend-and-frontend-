from sqlalchemy import Column, String, DateTime, ForeignKey
from app.models import Base
from datetime import datetime
import uuid

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    election_id = Column(String, ForeignKey("elections.id"), nullable=False)
    voter_id = Column(String, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(String, ForeignKey("candidates.id"), nullable=False)
    transaction_hash = Column(String, nullable=True)  # Blockchain transaction hash
    signature = Column(String, nullable=True)  # Voter signature (if applicable)
    created_at = Column(DateTime, default=datetime.utcnow)
