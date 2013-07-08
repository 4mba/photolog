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


_log_level_map = {
    'debug' : logging.DEBUG,
    'info' : logging.INFO,
    'warn' : logging.WARN,
    'error' : logging.ERROR,
    'critical' : logging.CRITICAL
    }

def _get_logger(logger_name, log_level='debug',
                log_filepath='photolog/resource/log/photolog.log'):
    my_logger = getLogger(logger_name);
    my_logger.setLevel(_log_level_map.get(log_level, 'warn'))
    
    formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    my_logger.addHandler(console_handler)
        
    file_handler = handlers.TimedRotatingFileHandler(log_filepath, when='D', interval=1)
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)
      
    return my_logger

photolog_logger = _get_logger('photolog_logger')



        
