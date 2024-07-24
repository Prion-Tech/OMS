import os

LOGGER_NAME = os.getenv('LOGGER_NAME', 'investment_bot_logger')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
HTTPX_TIMEOUT = int(os.getenv('HTTPX_TIMEOUT', '30'))
SENTRY_DSN = os.getenv('SENTRY_DSN', '')
APP_ENV = os.getenv('APP_ENV', 'prod')
APP_INSIGHT_CONNECTION_STRING = os.getenv('APP_INSIGHT_CONNECTION_STRING', '')
