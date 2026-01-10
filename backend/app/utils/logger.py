import logging
from loguru import logger

# Configure loguru
logger.remove()
logger.add("logs/app.log", rotation="500 MB", retention="10 days", level="INFO")
logger.add(lambda msg: print(msg, end=""), level="DEBUG")
