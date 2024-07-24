from fastapi import FastAPI

from app.config import APP_INSIGHT_CONNECTION_STRING, LOG_LEVEL, LOGGER_NAME
from GrantonLogTrace import granton_logging
from GrantonLogTrace.granton_tracing import GrantonTracing

logger = granton_logging.setup_logging(log_type='standard', log_level=LOG_LEVEL, logger_name=LOGGER_NAME)

# tracer = GrantonTracing(APP_INSIGHT_CONNECTION_STRING)


app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/health")
async def health_check():
    return {'status': 'OK'}
