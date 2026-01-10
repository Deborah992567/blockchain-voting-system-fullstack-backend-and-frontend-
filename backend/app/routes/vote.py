from fastapi import APIRouter

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("/submit-signature")
async def submit_signature():
    """Submit signed vote."""
    return {"message": "Not implemented"}
