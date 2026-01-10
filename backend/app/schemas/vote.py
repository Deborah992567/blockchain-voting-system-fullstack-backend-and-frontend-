from pydantic import BaseModel

class VoteBase(BaseModel):
    candidate_id: str

class VoteCreate(VoteBase):
    pass

class VoteResponse(VoteBase):
    id: str
    election_id: str
    voter_id: str
    transaction_hash: str

    class Config:
        from_attributes = True
