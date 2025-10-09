import logging
from pythonjsonlogger import jsonlogger

def configure_logging(level: str = "info"):
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "app"):
        logger = logging.getLogger(name)
        logger.handlers = [handler]
        logger.propagate = False
        logger.setLevel(level.upper())
