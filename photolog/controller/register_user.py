# -*- coding: utf-8 -*-
"""
    photolog.controller.register_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    사용자 등록 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from flask import render_template, request, redirect , url_for
from sqlalchemy.exc import IntegrityError
from werkzeug import generate_password_hash

from photolog.photolog_logger import photolog_logger
from photolog.photolog_blueprint import photolog
from photolog.database import dao
from photolog.model.user import User
from photolog.controller.login import login_required


@photolog.route('/user/regist/', methods=['GET', 'POST'])
def register_user():
    """포토로그 사용자 등록을 위한 함수"""
    
    # HTTP POST로 요청이 오면 사용자 정보를 등록
    if request.method == 'POST':
        
        password = request.form['password']
        password_confirm = request.form['password_confirm']
            
        username = request.form['username']
        email = request.form['email']

        if password == '' or password_confirm == '':
            error = "패스워드에 공백은 허용하지 않습니다."
            return render_template('regist.html', pass_error=error)  

        if password == password_confirm:
            try:
                user = User(username, email, generate_password_hash(password))
                dao.add(user)
                dao.commit()
    
                photolog_logger.debug(user) 
            except IntegrityError:
                error = "아이디(%s)가 중복됩니다.다른 아이디를 사용세요." % username
                photolog_logger.error(error)
                dao.rollback()
                return render_template('regist.html', id_error=error)
            except Exception as e:
                error = "DB error occurs : " + str(e)
                photolog_logger.error(error)
                dao.rollback()
                raise e
            else:
                # 성공적으로 사용자 등록이 되면, 로그인 화면으로 이동.
                return redirect(url_for('.login'))
        else:
            error = "패스워드가 일치하지 않습니다. 다시 입력해주세요."
            return render_template('regist.html', pass_error=error)
    #HTTP GET으로 요청이 오면 사용자 등록 화면을 보여줌
    else:
        return render_template('regist.html')


@photolog.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def modify_user(username=None):
    """포토로그 사용자 정보 수정을 위한 함수"""
    
    #HTTP POST로 요청이 오면 사용자 정보를 수정함
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        try:
            old_user = dao.query(User).filter_by(username=username).first()
    
            photolog_logger.debug(old_user)  
        except Exception as e:
            photolog_logger.error(str(e))
            raise e
                
        if password == '' or password_confirm == '':
            error = "패스워드에 공백은 허용하지 않습니다."
            return render_template('regist.html', user=old_user, pass_error=error)    
        if password == password_confirm:
            try:
                old_user.email = email
                old_user.password = generate_password_hash(password)
                dao.commit()

            except Exception as e:
                dao.rollback()
                photolog_logger.error(str(e))
                raise e
            else:
                # 성공적으로 사용자 등록이 되면, 로그인 화면으로 이동.
                return redirect(url_for('.login'))
        else:
            error = "패스워드가 일치하지 않습니다. 다시 입력해주세요."
            return render_template('regist.html', user=old_user, pass_error=error)
    #HTTP GET으로 요청이 오면 사용자 정보 수정 화면을 보여줌
    else:
        try:
            user = dao.query(User).filter_by(username=username).first()
            photolog_logger.debug(user) 
        except Exception as e:
            photolog_logger.error(str(e))
            raise e
        else:
            return render_template('regist.html', user=user)  

