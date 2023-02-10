import logging
from heapq import merge

from www.conf import config_default

configs = config_default.configs

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    # 格式化器
    'formatters': {
        'standard': {
            #
            #format中的这个mark没有，需要添加，作为日志编号
            'format':
                '[%(levelname)s] [%(asctime)s] [mark:%(mark)s] [%(filename)s] [%(funcName)s] [%(lineno)d] > %(message)s',
            "datefmt":
                "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format':
                '[%(levelname)s] > %(message)s',
            "datefmt":
                "%Y-%m-%d %H:%M:%S"
        },
    },
    # 处理器
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_handler': {
            'level': logging.INFO,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './log.txt',  # 具体日志文件的名字
            'maxBytes': 10*10*1024,
            'backupCount': 10,
            'formatter': 'standard'
        }  # 用于文件输出

    },
    # 日志记录器
    'loggers': {  # 日志分配到哪个handlers中
        'blogzzz': {  # 后面导入时logging.getLogger使用的app_name
            'handlers': ['console', 'file_handler'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
# try:
#    import config_override
#    configs = merge(configs, config_override.configs)
# except ImportError:
#    pass
