from fastapi import FastAPI

from GrantonLogTrace import granton_logging
from GrantonLogTrace.granton_tracing import GrantonTracing

from app.config import APP_INSIGHT_CONNECTION_STRING, LOGGER_NAME, LOG_LEVEL

logger = granton_logging.setup_logging(log_type='standard', log_level=LOG_LEVEL, logger_name=LOGGER_NAME)

# tracer = GrantonTracing(APP_INSIGHT_CONNECTION_STRING)


app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/health")
async def health_check():
    return {'status': 'OK'}
