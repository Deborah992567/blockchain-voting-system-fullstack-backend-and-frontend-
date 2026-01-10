from fastapi import APIRouter

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.get("")
async def list_candidates():
    """List all candidates."""
    return {"message": "Not implemented"}
