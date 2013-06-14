# -*- coding: utf-8 -*-
"""
    photolog.controller.register_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    사용자 등 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps

from photolog.photolog_blueprint import photolog
from photolog.database import DBManager
from photolog.model.user import User

@photolog.route('/register', methods=['GET', 'POST'])
def register_user():

    print "(%s)register_user invoked!" % (request.method)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password == password_confirm:
            try:
                user = User(username, email, password)
                DBManager.db_session.add(user)
                DBManager.db_session.commit()
    
                print user 
            except Exception as e:
                print "DB error occurs : " + str(e)
            else:
                # 성공적으로 사용자 등록이 되면, 로그인 화면으로 이동.
                return render_template('login.html')
        else:
            print "password confirmation failed!"
            redirect(url_for('.register_user'))
    
    else :   
        return render_template('register.html')

