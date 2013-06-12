# -*- coding: utf-8 -*-

"""
   photolog:__init__.py
    ~~~~~~~~~~~~~~

    photolog 어플리케이션 초기 셋

    :copyright: (c) 2013 by liks79 [http://www.github.com/liks79]
    :license: MIT LICENSE 2.0, see license for more details.
"""

from flask import Flask, render_template
from photolog.photolog_blueprint import photolog
from photolog.redis_session import RedisSessionInterface
from photolog.database import DBManager

# 추가할 controller 모듈을 import 해야만 어플리케이션에서 인식할 수 있음 
from photolog.controller import *

def create_app(config_filename='resource/config.cfg'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_filename)
    app.register_blueprint(photolog)
    app.session_interface = RedisSessionInterface()
    
    app.error_handler_spec[None][404] = not_found
    app.error_handler_spec[None][500] = server_error
    
    DBManager.init(app.config['DB_URL'])
    DBManager.init_db()
    
    return app

''' HTTP Error Code 404와 500은 errorhanlder에 application 레벨에서
    적용되므로 blueprint가 적용될 수 없으므로 app 객체 생성시 등록해준다.
    - by keaton
'''
def not_found(error):
#     print "404 Page not found"
    return render_template('404.html')

def server_error(error):
#     print "500 Server Error"
    return render_template('500.html')

