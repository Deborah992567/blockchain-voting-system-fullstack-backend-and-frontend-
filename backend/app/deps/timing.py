from fastapi import Request
import time
from app.utils.logger import logger

async def timing_dependency(request: Request):
    request.state.start_time = time.time()
    return request
