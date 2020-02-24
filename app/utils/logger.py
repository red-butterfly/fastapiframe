# -*- coding: utf-8 -*-
'''
created by hanfei on 17/8/29
'''
import logging
from logging.handlers import TimedRotatingFileHandler
from cloghandler import ConcurrentRotatingFileHandler


_logger_level = {
    'fatal': logging.FATAL,
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}


def initLoggerByTime(name ,filename, log_level="INFO", when='D', interval=1, backupCount=60,
               format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'):
    '''
    "S"：Second 秒; "M"：Minutes 分钟; "H"：Hour 小时; "D"：Days 天;"W"：Week day（0 = Monday）
    :param name:
    :param filename:
    :param log_level:
    :param when:
    :param interval:
    :param backupCount:
    :param format:
    :return:
    '''
    # 默认的日志为 INFO，各模块的输出日志等级在 params中定义：(DEBUG/INFO/WARNING/ERROR/CRITICAL
    logging.basicConfig(level=_logger_level[log_level], format=format)
    handler = TimedRotatingFileHandler(filename, when, interval, backupCount)
    handler.suffix = "%Y-%m-%d.log"
    handler.setLevel(_logger_level[log_level])
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    # console = logging.StreamHandler()
    # console.setLevel(_logger_level[log_level])  

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    # logger.addHandler(console)
    return handler


def initLoggerBySize(name ,filename, log_level="INFO", size=1024*1024, backup_count=20,
               format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'):
    '''
    "S"：Second 秒; "M"：Minutes 分钟; "H"：Hour 小时; "D"：Days 天;"W"：Week day（0 = Monday）
    :param name:
    :param filename:
    :param log_level:
    :param when:
    :param interval:
    :param backupCount:
    :param format:
    :return:
    '''
    # 默认的日志为 INFO，各模块的输出日志等级在 params中定义：(DEBUG/INFO/WARNING/ERROR/CRITICAL
    re_filename = f'{filename}.log'
    logging.basicConfig(level=_logger_level[log_level], format=format)
    rotateHandler = ConcurrentRotatingFileHandler(re_filename, "a", size, backup_count)
    rotateHandler.setLevel(_logger_level[log_level])
    formatter = logging.Formatter(format)
    rotateHandler.setFormatter(formatter)

    # console = logging.StreamHandler()
    # console.setLevel(_logger_level[log_level])  

    logger = logging.getLogger(name)
    logger.addHandler(rotateHandler)
    # logger.addHandler(console)
    return rotateHandler


def initLogger_flask(filename, log_level="INFO", when='D', interval=1, backupCount=60,
               format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'):
    '''
    针对flask，只返回handler
        "S"：Second 秒; "M"：Minutes 分钟; "H"：Hour 小时; "D"：Days 天;"W"：Week day（0 = Monday）
        :param name:
        :param filename:
        :param log_level:
        :param when:
        :param interval:
        :param backupCount:
        :param format:
        :return:
    '''
    # 默认的日志为 INFO，各模块的输出日志等级在 params中定义：(DEBUG/INFO/WARNING/ERROR/CRITICAL
    logging.basicConfig(level=_logger_level[log_level], format=format)
    handler = TimedRotatingFileHandler(filename, when, interval, backupCount)
    handler.setLevel(_logger_level[log_level])
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    return handler
