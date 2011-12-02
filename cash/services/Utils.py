from django.db import connection
import logging
import logging.handlers
from django.conf import settings

def show_sql():
    print connection.queries
    #cols, sql, args = q._get_sql_clause()
    #return "SELECT %s %s" % (', '.join(cols), sql % tuple(args))

def get_logger():
    logger = logging.getLogger('cash-logger')
    logger.setLevel(settings.LOG_LEVEL)
    handler = logging.handlers.RotatingFileHandler(
              settings.LOG_FILE, maxBytes=2097152, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
    