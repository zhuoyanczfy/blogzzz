import logging
import logging.config
import aiotask_context as context

from www.conf.config import LOG_CONFIG


class LogMarkFilter(logging.Filter):
    def filter(self, record):
        try:
            record.mark = context.get("task_mark") or context.get("view_mark")
        except (ValueError, AttributeError):
            record.mark = ''
        return True

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("blogzzz") #这个和LOG_CONFIG中的logger名称相同，切记！
logger.addFilter(LogMarkFilter())
logger.debug('debug message')