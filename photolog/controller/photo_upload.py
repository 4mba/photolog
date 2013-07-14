# -*- coding: utf-8 -*-
"""
    photolog.controller.upload_files
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    파일 업로드 모듈.
    사진을 어플리케이션 서버의 임시 디렉터리에 저장함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


import os
from flask import request, redirect, url_for, current_app, send_from_directory \
				, render_template, session
from werkzeug.utils import secure_filename

from photolog.database import DBManager
from photolog.model.photo import Photo
from photolog.controller.login import login_required
from photolog.photolog_logger import photolog_logger

from photolog.photolog_blueprint import photolog
from datetime import datetime
import uuid



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@photolog.route('/photo/upload')
@photolog.route('/photo/upload/<filename>')
@login_required
def upload_form(filename=None):
    return render_template('upload.html', filename=filename)


@photolog.route('/photo/upload', methods=['POST'])
@login_required
def upload_photo():

    userid = session['user_info'].username
    tag = request.form['tag']
    comment = request.form['memo']
    lat = request.form['lat']
    lng = request.form['lng']
    upload_date = datetime.today()
    taken_date = datetime.strptime(request.form['date'], "%Y:%m:%d %H:%M:%S");
    upload_photo = request.files['upload']
    
    filename = None
    filesize = 0

    # 파일 업로드시 발생하는 예외 처리
    try:
        if upload_photo and allowed_file(upload_photo.filename):
            # secure_filename은 한글 지원 안됨
            filename111 = secure_filename(unicode(upload_photo.filename))
            print filename111
            
            ext = (upload_photo.filename).rsplit('.', 1)[1]
            filename = userid +'_'+ unicode(uuid.uuid4()) + '.' + ext
            upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            upload_photo.save(os.path.join(upload_folder, filename))
            filesize = os.stat(upload_folder+filename).st_size

        else:
            raise Exception("File uoload error : illegal file.")
    except Exception as e:
        photolog_logger.error("Upload error : " + str(e))


    # DB에 저장할 때 발생하는 예외 처리
    try :
        photo = Photo(userid, tag, comment, filename, filesize, lat, lng, upload_date, taken_date)
        dao = DBManager.db_session
        dao.add(photo)
        dao.commit()

    except Exception as e:
        dao.rollback()
        photolog_logger.error("Upload DB error : " + str(e))

    return redirect(url_for('.show_all'))



@photolog.route('/photo/modify/<photolog_id>')
@login_required
def modify(photolog_id):
    dao = DBManager.db_session
    photo = dao.query(Photo).filter_by(id=photolog_id).first()
    
    return render_template('upload.html', photo=photo)




