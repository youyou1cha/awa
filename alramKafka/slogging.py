import logging
from logging.handlers import TimedRotatingFileHandler
import sys

def setup_logging(log_file):
    # 创建Logger对象
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # 创建TimedRotatingFileHandler对象
    handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=5)
    handler.setLevel(logging.DEBUG)

    # 设置日志输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    # 将处理器添加到Logger对象
    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    return logger

# 使用示例
logger = setup_logging('my_log.log')
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
