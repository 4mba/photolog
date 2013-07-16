# -*- coding: utf-8 -*-
"""
    photolog.photolog_logger
    ~~~~~~~~

    photolog 로그 모듈. 
    photolog 어플리케이션에서 사용할 공통 로그 객체를 생성.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import logging
from logging import getLogger, handlers, Formatter


class Log:
    _log_level_map = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error' : logging.ERROR,
        'critical' : logging.CRITICAL
        }
    
    _my_logger=None
    
    @staticmethod
    def init(logger_name='photolog', log_level='debug',
                    log_filepath='photolog/resource/log/photolog.log'):
        Log._my_logger = getLogger(logger_name);
        Log._my_logger.setLevel(Log._log_level_map.get(log_level, 'warn'))
        
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        Log._my_logger.addHandler(console_handler)
            
        file_handler = handlers.TimedRotatingFileHandler(log_filepath, when='D', interval=1)
        file_handler.setFormatter(formatter)
        Log._my_logger.addHandler(file_handler)
          
#         return my_logger
    
    @staticmethod
    def debug(msg):
        Log._my_logger.debug(msg)
    
    @staticmethod
    def info(msg):
        Log._my_logger.info(msg)
    
    @staticmethod
    def warn(msg):
        Log._my_logger.warn(msg)
    
    @staticmethod
    def error(msg):
        Log._my_logger.error(msg)
    
    @staticmethod
    def critical(msg):
        Log._my_logger.critical(msg)

photolog_logger = None
# 
# from photolog import photolog_app
# photolog_logger = _get_logger('photolog_logger'
#                             , photolog_app.config['LOG_LEVEL'])



        
