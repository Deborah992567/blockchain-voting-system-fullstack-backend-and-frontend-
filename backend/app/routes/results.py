from fastapi import APIRouter

router = APIRouter(prefix="/results", tags=["results"])

@router.get("")
async def get_results():
    """Get election results."""
    return {"message": "Not implemented"}
