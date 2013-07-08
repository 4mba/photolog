# -*- coding: utf-8 -*-
"""
    photolog.blueprint
    ~~~~~~~~~~~~~~~~~~

    photolog 어플리케이션에 적용할 blueprint 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import Blueprint
from photolog.photolog_logger import photolog_logger

photolog = Blueprint('photolog', __name__,
                     template_folder='../templates', static_folder='../static')

photolog_logger.info('static folder : %s' % photolog.static_folder)
photolog_logger.info('template folder : %s' % photolog.template_folder)
