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


@photolog.teardown_request
def close_db_session(exception=None):
    """요청이 완료된 후에 db연결에 사용된 세션을 종료함"""
    
    try:
        DBManager.db_session.remove()
    except Exception as e:
        photolog_logger.error(str(e))


def login_required(f):
    """현재 사용자가 로그인 상태인지 확인하는 데코레이터
    로그인 상태에서 접근 가능한 함수에 적용함
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_key = request.cookies.get(current_app.config['SESSION_COOKIE_NAME'])

            is_login = False
            if session.sid == session_key and session.__contains__('user_info') :
                is_login = True

            if not is_login:
                return redirect(url_for('.login', next=request.url))

            return f(*args, **kwargs)

        except Exception as e:
            photolog_logger.error("Login error occurs : %s" % str(e))
            raise e

    return decorated_function


@photolog.route('/')
@login_required
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return redirect(url_for('.show_all'))


@photolog.route('/user/login', methods=['GET', 'POST'])
def login():
    """아이디/패스워드 기반의 로그인 기능을 제공함
    로그인 성공 시 세션에 사용자 정보를 저장하여 사용함
    """
    
    session.permanent = True
    dao = DBManager.db_session

    login_error = None
    next_url = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:
            user = dao.query(User).filter_by(username=username).first()
        except Exception as e:
            photolog_logger.error(str(e))
            raise e

        if user:
            if username != user.username or not check_password_hash(user.password, password):
                login_error = 'Invalid username or  password'
            else:
                if request.form['next']:
                    next_url = request.form['next']
                    photolog_logger.info("(%s)next_url is %s" % (request.method, next_url))
                # 세션에 추가할 정보를 session 객체의 값으로 추가함
                # 가령, UserInfo 클래스 같은 사용자 정보를 추가하는 객체 생성하고
                # 사용자 정보를 구성하여 session 객체에 추가
                session['user_info'] = user
                photolog_logger.info("(%s)next_url is %s" % (request.method, next_url))
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(url_for('.index'))
                    
        else:
            login_error = 'User does not exist!'

    elif request.method == 'GET':
        next_url = request.args.get('next', None)
        photolog_logger.info("(%s)next_url is %s" % (request.method, next_url))

    return render_template('login.html', next=next_url, error=login_error)


@photolog.route('/logout')
def logout():
    """로그아웃 시에 호출되며 세션을 초기화함"""
    
    session.clear()

    return redirect(url_for('.index'))

