# -*- coding: utf-8 -*-
"""
   manager.py
    ~~~~~~~~~~~~~~

    Controller 

    :copyright: (c) 2013 by liks79 [http://www.github.com/liks79]
    :license: MIT LICENSE 2.0, see license for more details.
"""


from application import app
from flask import render_template, request, redirect, url_for, jsonify




@app.route('/index/')
@app.route('/')
def index():

    return render_template('main/list.jade', title='제안 목록',this_year=this_year,feedbacks = feedbacks, has_next = has_next, next_page = 2, tab_name = 'all')


@app.route('/login/', methods=['POST'])
def login():
    
    return render_template('main/list.jade', title='제안 목록',this_year=this_year,feedbacks = feedbacks, has_next = has_next, next_page = 2, tab_name = 'all')



