from pydantic import BaseModel
from datetime import datetime

class ElectionBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class ElectionCreate(ElectionBase):
    pass

class ElectionResponse(ElectionBase):
    id: str
    is_active: bool
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True
