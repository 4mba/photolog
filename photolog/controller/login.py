# -*- coding: utf-8 -*-
"""
    photolog.controller.login
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    로그인 확인 데코레이터와 로그인 처리 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import render_template, request, current_app, session, redirect \
                 , url_for
from functools import wraps
from werkzeug import check_password_hash

from photolog.photolog_logger import photolog_logger
from photolog.photolog_blueprint import photolog
from photolog.database import DBManager
from photolog.model.user import User
from photolog.model.photo import Photo

''' 로긴이 필요한 페이지에 decorating '''
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_key = request.cookies.get(current_app.config['SESSION_COOKIE_NAME'])

#             print "session : %s" % session
            is_login = False
            if session.sid == session_key and session.__contains__('user_info') :
                is_login = True

            if not is_login:
                return redirect(url_for('.login', next=request.url))

            return f(*args, **kwargs)

        except Exception as e:
            print "Login error occurs : %s" % str(e)

    return decorated_function


@photolog.route('/')
# 로그인 하지 않아도 페이지가 보이도록 수정
@login_required
def index():
    print "index invoked!"
    dao = DBManager.db_session
    
    return render_template('entry_all.html', photos=dao.query(Photo).order_by(Photo.upload_date.desc()).all())


@photolog.route('/user/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    dao = DBManager.db_session

    login_error = None
    next_url = None
    print "(%s)login invoked!" % (request.method)
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:
            user = dao.query(User).filter_by(username=username).first()
        except Exception as e:
            photolog_logger.error(str(e))
            raise Exception(e)

        if user is not None:
            
            if username != user.username or not check_password_hash(user.password, password):
                login_error = 'Invalid username or  password'
            else:
                if request.args.__contains__('next'):
                    next_url = request.args['next']
                    print "(%s)next_url is %s" % (request.method, next_url)
                # 세션에 추가할 정보를 session 객체의 값으로 추가함
                # 가령, UserInfo 클래스 같은 사용자 정보를 추가하는 객체 생성하고
                # 사용자 정보를 구성하여 session 객체에 추가
                session['user_info'] = user

                if next_url is None:
                    return redirect(url_for('.index'))
                else:
                    return redirect(next_url)
        else:
            login_error = 'User does not exist!'

    elif request.method == 'GET':
        next_url = request.args.get('next', None)
        print "(%s)next_url is %s" % (request.method, next_url)

    return render_template('login.html', next=next_url, error=login_error)


@photolog.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('.index'))

