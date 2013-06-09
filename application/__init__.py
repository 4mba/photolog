# -*- coding: utf-8 -*-

"""
   application:__init__.py
    ~~~~~~~~~~~~~~

    photolog 어플리케이션 초기 셋

    :copyright: (c) 2013 by liks79 [http://www.github.com/liks79]
    :license: MIT LICENSE 2.0, see license for more details.
"""
from flask import Flask, render_template
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
print '[template directory] ' + tmpl_dir
print '[static directory] ' + static_dir

app = Flask(__name__, static_folder=static_dir, template_folder=tmpl_dir)


@app.errorhandler(404)
def not_found(error):
    print "404 Page not found"
    return render_template('404.html')

@app.errorhandler(500)
def server_error(error):
    print "500 Server Error"
    return render_template('500.html')

