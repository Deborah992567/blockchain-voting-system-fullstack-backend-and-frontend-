from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.election import Election
from app.schemas.election import ElectionCreate, ElectionResponse
from app.database.session import get_db
from app.auths.routes import get_current_user
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/elections", tags=["elections"])

@router.post("", response_model=ElectionResponse)
async def create_election(
    election: ElectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new election."""
    new_election = Election(
        title=election.title,
        description=election.description,
        start_time=election.start_time,
        end_time=election.end_time,
        created_by=current_user.id
    )
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election

@router.get("", response_model=list[ElectionResponse])
async def list_elections(db: Session = Depends(get_db)):
    """List all elections."""
    elections = db.query(Election).all()
    return elections

@router.get("/{election_id}", response_model=ElectionResponse)
async def get_election(election_id: str, db: Session = Depends(get_db)):
    """Get election details."""
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(status_code=404, detail="Election not found")
    return election
