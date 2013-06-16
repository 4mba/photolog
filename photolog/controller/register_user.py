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


@photolog.route('/register/', methods=['GET', 'POST'])
@photolog.route('/register/<user>', methods=['GET', 'POST'])
def register_user(user=None):

    print "(%s)register_user invoked!" % (request.method)
    if request.method == 'POST':
        
        password = request.form['password']
        password_confirm = request.form['password_confirm']
            
        if user is None:
            username = request.form['username']
            email = request.form['email']

            if password == password_confirm:
                try:
                    user = User(username, email, password)
                    DBManager.db_session.add(user)
                    DBManager.db_session.commit()
        
                    print user 
                except Exception as e:
                    error = "DB error occurs : " + str(e)
                    print error
                    return render_template('register.html', error=error)
                else:
                    # 성공적으로 사용자 등록이 되면, 로그인 화면으로 이동.
                    return redirect(url_for('.login'))
            else:
                error = "password confirmation failed!"
                print "Register user error : %s" % error
                return render_template('register.html', error=error)
        # 사용자 정보 DB에 업데이트(HTTP PUT 처리를 대신함)
        else:
            if password == password_confirm:
                print "modifying user info..."
                try:
                    old_user = DBManager.db_session.query(User).filter_by(username=user).first()
                    old_user.password = password
                    
                    DBManager.db_session.commit()
        
                    print user 
                except Exception as e:
                    error = "DB error occurs : " + str(e)
                    print error
                    return render_template('register.html', error=error)
                else:
                    # 성공적으로 사용자 등록이 되면, 로그인 화면으로 이동.
                    return redirect(url_for('.login'))
            else:
                error = "password confirmation failed!"
                print "Register user error : %s" % error
                return render_template('register.html', error=error)
    
    else:
        # 초기 사용자 등록 화면
        if not user:
            return render_template('register.html')
        # 사용자 정보 수정 화면
        else:
            print "editing user info..."
            try:
                user = DBManager.db_session.query(User).filter_by(username=user).first()
    
                print user 
            except Exception as e:
                print "DB error occurs : " + str(e)
                return render_template('register.html', error=error)
            else:
                return render_template('register.html', user=user)   


