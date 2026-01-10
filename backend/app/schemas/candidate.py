from pydantic import BaseModel

class CandidateBase(BaseModel):
    name: str
    description: str

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: str
    election_id: str
    user_id: str

    class Config:
        from_attributes = True
