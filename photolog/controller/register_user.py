# -*- coding: utf-8 -*-
"""
    photolog.controller.register_user
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    사용자 등록 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import os
from flask import render_template, request, redirect , url_for, session, current_app
from sqlalchemy.exc import IntegrityError
from werkzeug import generate_password_hash

from photolog.photolog_logger import Log
from photolog.photolog_blueprint import photolog
from photolog.database import dao
from photolog.model.user import User
from photolog.controller.login import login_required


@photolog.route('/user/regist', methods=['POST', 'GET'])
def register_user():
    """포토로그 사용자 등록을 위한 함수"""
    print "%s invoked!" % request.method
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
            
                Log.debug(user) 
            except IntegrityError:
                error = "아이디(%s)가 중복됩니다.다른 아이디를 사용세요." % username
                Log.error(error)
                dao.rollback()
                return render_template('regist.html', id_error=error)
            except Exception as e:
                error = "DB error occurs : " + str(e)
                Log.error(error)
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
    
            Log.debug(old_user)  
        except Exception as e:
            Log.error(str(e))
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
                Log.error(str(e))
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
            Log.debug(user) 
        except Exception as e:
            Log.error(str(e))
            raise e
        else:
            return render_template('regist.html', user=user)


@photolog.route('/user/unregist')
@login_required
def unregist():
    user_id = session['user_info'].id
    try:
        user = dao.query(User).filter_by(id=user_id).first()
        if user.id == user_id:
            dao.delete(user)
            # 업로드된 사진 파일 삭
            try:
                upload_folder = os.path.join(current_app.root_path, 
                                             current_app.config['UPLOAD_FOLDER'])
                __delete_files(upload_folder, user.username)
            except Exception as e:
                Log.error("파일 삭제에 실패했습니다. 나중에 일괄 삭제하세요. : %s" + str(e))
            
            dao.commit()
        else:
            Log.error("존재하지 않는 사용자의 탈퇴시도 : %d", user_id)
            raise Exception
    except Exception as e:
        Log.error(str(e))
        dao.rollback()
        raise e
    else:
        return redirect(url_for('.login'))

def __delete_files(filepath, username):
    import glob
    del_filepath_rule = filepath  + username + "_*"
    files = glob.glob(del_filepath_rule)
    for f in files:
        Log.debug(f)
        os.remove(f)

